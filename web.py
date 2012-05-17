# Secret-Service-Chat
# Author: Ryan McGowan
#
# Version:
version = "0.1.0"

import os

from secret_service.config import read_system_config, init_logging
import secret_service.model as model
from flask import (Flask, send_from_directory, render_template, redirect,
        request, url_for, jsonify)
from sys import argv

#Create the app
app = Flask(__name__)

#Run various initilization functions.
read_system_config(app, argv)
init_logging(app)


#For browsers that do not support the link tag for favicon
@app.route('/favicon.ico')
def favicon():
    """Reroute requests to the favicon to the correct location in static."""
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/')
def index():
    """Render the site homepage, which is also the search page."""
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    return redirect(request.args.get("next") or url_for("index"))


@app.route('/message', methods=["GET", "POST"])
def get_message():
    return {}


@app.route('/message', methods=["PUT"])
def put_message():
    result = model.add_new_message(request)
    app.logger.debug(result)
    return jsonify(result)


def run_application():
    if app.is_production:
        address = "0.0.0.0"
        port = int(os.environ.get("PORT", 5000))
    else:
        address = "127.0.0.1"
        port = int(os.environ.get("PORT", 5000))

    app.logger.info("Starting the Super Secret Service Char Server " + version)
    app.run(address, port)


if __name__ == '__main__':
    run_application()
