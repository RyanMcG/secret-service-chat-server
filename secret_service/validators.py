from secret_service.utils import to_uuid
from secret_service import model
import re
import rsa
import base64


def merge_errors(success, errors, result):
    """Merges errors and success with those from result."""
    errors.extend(result[1])
    return success and result[0]


def keys_are_uuids(data, keys):
    """Cheks that the given keys in the data map are all valid uuids."""
    success = True
    errors = []
    for k in keys:
        uuid = to_uuid(data[k])
        if not uuid:
            success = False
            errors.append({
                'type': 'FATAL',
                'cause':
                "%s is not a valid UUID." % k})
    return (success, errors)


def new_message_request(data):
    """Verifies that the given dict represents a valid message."""
    success = True
    errors = []
    dkeys = data.keys()
    req_keys = ['receiver_id', 'sender_id', 'receiver_key_id', 'sender_key_id',
            'message', 'signature']

    # First thing is to ensure that the keys in the given data dict match the
    # expected keys exactly.
    if set(dkeys) != set(req_keys):
        success = False
        errors.append({
            'type': 'FATAL',
            'cause':
            "Keys in request (%s) do not match required keys (%s)." % \
                    (str(dkeys), str(req_keys))})
    else:
        # Helper function to verify subset of keys are uuids.
        success = merge_errors(success, errors, keys_are_uuids(data,
            req_keys[:4]))
        if success:
            # All uuid fields are valid.
            for k in req_keys[:2]:
                if not model.user_exists(to_uuid(data[k])):
                    success = False
                    errors.append({
                        'type': 'FATAL',
                        'cause': "The user (%s) does not exist." % data[k]})
            if success:
                # All users are valid
                for k in req_keys[2:4]:
                    # Check that given keys exist
                    user_id = to_uuid(data[k[:-6] + 'id'])
                    user_key_id = to_uuid(data[k])
                    keys = model.get_user_key(user_id)
                    if user_key_id not in keys:
                        success = False
                        errors.append({
                            'type': 'FATAL',
                            'cause': "Invalid key_id (%s) for %s." % (
                                user_key_id, user_id)})
    return (success, errors)


def is_public_key(key):
    """Returns whether or not the given key is a valid RSA public key."""
    # TODO Implement
    try:
        rsa.PublicKey.load_pkcs1(base64.b64decode(key), 'DER')
        return True
    except Exception:
        return False


def check_user_keys(user_doc):
    """Check that all keys in the given dict are valid for a user."""
    success = True
    errors = []

    user_keys = ['username', 'keys', 'name']
    req_keys = user_keys[:2]
    # Check that all required fields exist
    for k in req_keys:
        if k not in user_doc:
            success = False
            errors.append({'type': 'FATAL',
                'cause': "Required key (%s) not found in request body." % k})
    # Ensure that only valid keys exist
    for k in user_doc:
        if k not in user_keys:
            success = False
            errors.append({'type': 'FATAL',
                'cause': "Invalid key (%s) in request body." % k})
    return (success, errors)


def new_user(user_doc):
    """Validates the given new user."""
    # Continue searching for validation issues if no problems have been
    # encountered yet
    errors = []
    success = merge_errors(True, errors, check_user_keys(user_doc))
    if success:
        # No errors yet, so all keys are valid and exist.
        if not re.match(r'^[a-zA-Z][a-zA-Z_\-0-9]*[a-zA-Z0-9]$',
                user_doc['username']):
            success = False
            errors.append({'type': 'FATAL',
                'cause': "Username (%s) is invalid." % user_doc['username']})
        if not re.match(r'^[a-zA-Z][a-zA-Z ]+[a-zA-Z]$', user_doc['name']):
            success = False
            errors.append({'type': 'FATAL',
                'cause': "Name (%s) is invalid." % user_doc['name']})
        if len(user_doc['keys']) <= 0:
            success = False
            errors.append({'type': 'FATAL',
                'cause': "User must have at least 1 key."})
        else:
            for pk in user_doc['keys']:
                if not is_public_key(pk):
                    success = False
                    errors.append({
                        'type': 'FATAL',
                        'cause': "Given public key (%s) is invalid." % pk})
    return (success, errors)
