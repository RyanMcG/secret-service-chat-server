from secret_service import model, validators as is_valid
from pymongo.errors import OperationFailure
from uuid import UUID


def register_user(user):
    """Registers the given user."""
    (success, errors) = is_valid.new_user(user)

    try:
        uuid = model.add_user(user) if success else None
    except OperationFailure:
        success = False
        uuid = None
        errors.append({'type': 'FATAL',
                'cause': ("A user with the username ({0}) already exists"
                    ).format(user['username'])})
    result = {
            'success': success,
            'user_id': uuid}
    if len(errors) > 0:
        result['errors'] = errors

    return result


def add_new_message(data):
    """Adds a the given message to the messages index if it is valid."""
    # TODO: Clean this up. Some of the ugliest code I've ever written. Probably
    # should separate model accessing functions from busniess logic so the
    # validator can use model functions.

    # Desribe a default map to return
    result = {
            'success': True}
    (result['success'], errors) = is_valid.new_message_request(data)
    if result['success']:
        # If we still haven't found any errors we can add the message to
        # the database.
        msg_id = model.add_message(data)
    else:
        msg_id = None
    result['message_id'] = msg_id
    # If we found any errors add them to the response.
    if len(errors) > 0:
        result['errors'] = errors
    return result


def get_user_keys(user_id):
    """Get's the keys for specified user."""
    return model.get_user_keys(user_id)


def get_key(key_id):
    """Get's the key with the given key_id."""
    try:
        key = model.get_key(UUID(key_id))
    except ValueError:
        key = model.get_key(key_id)
    if key != None:
        del key['_id']
    if key:
        result = {
                'success': True,
                'key': key}
    else:
        result = {
                'success': False,
                'errors': [{
                    'type': 'FATAL',
                    'cause': 'Could not find a key with the given id (%s).' %
                    (key_id)}],
                'key': None}

    return result


def get_messages(user_id):
    """Get's messages for the specified user."""
    result = {
            'success': True,
            'messages': []}
    if model.user_exists(UUID(user_id)):
        # Get messages for the specified user_id
        msgs = model.get_messages(UUID(user_id))
        result['messages'] = [x for x in msgs]
    else:
        result['success'] = False
    return result
