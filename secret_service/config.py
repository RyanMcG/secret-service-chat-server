from os import path, environ


def read_system_config(app, cliargs):
    """Read system configuration from file and fallback on env variables."""
    from yaml import load

    server_type = "development"  # The default server type
    #Set Timed Logger rotation interval
    app.config['LOGGER'] = {'INTERVAL_TYPE': 'D', 'INTERVAL_COUNT': 7}

    # If we were pased in a cli argument parst it as the server_type
    if len(cliargs) > 1:
        server_type = cliargs[1].lower()
    elif "BITS_BOOKS_SERVER_TYPE" in environ:
        #Check to see if an environment variable specifies server_type
        server_type = environ.get("BITS_BOOKS_SERVER_TYPE")
    else:
        app.logger.warning("Could not determine server type. Defaulting to '" +
                server_type + "'.")

    app.is_production = server_type == "production"

    app.logger.info("Running as production . . ." if app.is_production else
            "Running in dev mode . . .")

    #Based on the server_type set up some other variables.
    app.debug = not app.is_production

    try:
        config_file = open(path.join(app.root_path, 'config.yml'))
        config = load(config_file)
        app.secret_key = config['application']['secret_key']
    except IOError:
        app.logger.info("'config.yml' not found. Checking environment.")
        # There is no config.yml file so check to see if we can use environment
        # variables.
        if "SECRET_SERVICE_SECRET_KEY" in environ:
            app.secret_key = environ.get("SECRET_SERVICE_SECRET_KEY")
        else:
            app.logger.critical("SECRET_SERVICE_SECRET_KEY is not specified by"
                    "the environment")
            raise RuntimeWarning("Could not set the secret key. "
                    "(No configuration.")


def init_logging(app):
    """Adds some handlers to the default logger."""
    if not app.is_production:
        from logging.handlers import TimedRotatingFileHandler
        from logging import Formatter

        handlers = []
        #Create timed, rotating file handler.
        logFileName = 'production.log' if app.is_production else \
                'development.log'
        logFilePath = path.join(app.root_path, 'logs/' + logFileName)
        thandler = TimedRotatingFileHandler(logFilePath,
                when=app.config['LOGGER']['INTERVAL_TYPE'],
                interval=app.config['LOGGER']['INTERVAL_COUNT'])
        thandler.setFormatter(Formatter("%(asctime)s %(levelname)s: " +
                "%(message)s [in %(pathname)s:%(lineno)d]"))
        handlers.append(thandler)

        for handler in handlers:
            app.logger.addHandler(thandler)
