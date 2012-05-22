# Secret-Service-Chat
# Author: Ryan McGowan
#
# Version:
version = "0.1.0"

import os

from secret_service.config import read_system_config, init_logging
import secret_service.model as model
from secret_service.utils import describe_request as describe
from flask import (Flask, send_from_directory, render_template, redirect,
        request, url_for, jsonify)
from flask import json as jm
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
    #return model.get_messages(request
    return jsonify({})


@app.route('/message', methods=["PUT"])
def put_message():
    app.logger.debug("Attempting to add new message (" + describe(request) + \
            ") to message store.")

    # Set the request data
    if request.json:
        request_data = request.json
    else:
        jd = jm.JSONDecoder()
        try:
            request_data = jd.decode(request.data)
        except ValueError:
            request_data = {}

    # Try adding the message with the given data
    result = model.add_new_message(request_data)

    if not result['success']:
        # The message was not added
        app.logger.debug("Failed adding new message: " + str(result))
    else:
        # Everything went as expected!
        app.logger.debug("Successfully added new message: " + str(result))
    return jsonify(**result)


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
