# Secret-Service-Chat
# Author: Ryan McGowan
#
# Version:
version = "0.2.0"

import os

from secret_service.config import read_system_config, init_logging
from secret_service import chat, model
from secret_service.utils import describe_request as describe, jsonit
from flask import Flask, send_from_directory, render_template, request
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


@app.route('/user', methods=["PUT"])
def put_user():
    """Put user function registers the user in the request body and returns the
    response as JSON."""
    result = chat.register_user(request.json)
    return jsonit(result)


@app.route('/keys/<username>', methods=["GET"])
def get_keys(username):
    user_id = model.get_user(username, ['_id'])
    if not user_id:
        result = {
                'success': False,
                'keys': [],
                'errors': [{
                    'type': 'FATAL',
                    'cause': 'Unable to find user with username (%s).' % \
                            username}]}
    else:
        result = {
                'success': True,
                'keys': [x for x in chat.get_user_keys(user_id['_id'])]}
    return jsonit(result)


@app.route('/key/<key_id>', methods=["GET"])
def get_key(key_id):
    return jsonit(chat.get_key(key_id))


@app.route('/message/<user_id>', methods=["GET"])
def get_message(user_id):
    result = chat.get_messages(user_id)
    return jsonit(result)


@app.route('/message', methods=["PUT"])
def put_message():
    app.logger.debug("Attempting to add new message (" + describe(request) + \
            ") to message store.")

    # Try adding the message with the given data
    result = chat.add_new_message(request.json)

    if not result['success']:
        # The message was not added
        app.logger.debug("Failed adding new message: " + str(result))
    else:
        # Everything went as expected!
        app.logger.debug("Successfully added new message: " + str(result))
    return jsonit(result)


@app.route('/test_message', methods=["GET"])
def temp_test_message():
    return jsonit({'messages': [x for x in model.db.messages.find()]})


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
