from bson.objectid import ObjectId
import rsa

def object_id(oid):
    """Takes an bson ObjectId and check whether it is valid or not."""
    try:
        ObjectId(oid)
        return True
    except InvalidId:
        return False

def new_message_request(data):
    success = True
    errors = []

    # Run a few simple checks to make sure the given request has the necessary
    # fields.
    if not (data.has_key('receiver_id') and object_id(data['receiver_id'])):
        success = False
        errors.append({
            'type': 'FATAL',
            'cause': '\'receiver_id\' does not exist or it is invalid.'})
    if not (data.has_key('sender_id') and object_id(data['sender_id'])):
        success = False
        errors.append({
            'type': 'FATAL',
            'cause': '\'sender_id\' does not exist or it is invalid.'})
    if not data.has_key('message'):
        errors.append({
            'type': 'FATAL',
            'cause': '\'message\' does not exist.'})

    return (success, errors)
