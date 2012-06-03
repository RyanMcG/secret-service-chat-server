from secret_service import model, validators as is_valid


def register_user(user):
    """Registers the given user."""
    (success, errors) = is_valid.new_user(user)

    uuid = model.add_user(user) if success else None
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
            'success': True,
            'data': data}
    (result['success'], errors) = is_valid.new_message_request(data)
    if result['success']:
        # If we still haven't found any errors we can add the message to
        # the database.
        model.add_message(data)

    # If we found any errors add them to the response.
    if len(errors) > 0:
        result['errors'] = errors
    return result


def get_messages(user_id):
    """Get's messages for the specified user."""
    result = {
            'success': True,
            'messages': []}
    if model.user_exists(user_id):
        msg_ids = []
        # Get messages for the specified user_id
        msgs = model.get_messages(user_id)
        for msg in msgs:
            # Keep track of each id accessed
            msg_ids.append(msg['_id'])
            # Remove the id field from each message dict
            del msg['_id']
        # Remove messages so they do not persist in the database.
        # TODO: Implementation requiest working authentication.
        #model.remove_messages(msg_ids)
        result['messages'] = msgs
    else:
        result['success'] = False
    return result
