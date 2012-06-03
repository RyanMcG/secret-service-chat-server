from os import environ
from pymongo import Connection
from urlparse import urlparse
from uuid import UUID
from secret_service import science
import uuid


# `db` is the mongodb database used by this application. It should have the
# following collections:
#
#   cipthertexts - Contains documents like:
#       {
#           sender_id: ObjectId('...'),
#           sender_key_id: "ask38fsk3"
#           receiver_id: ObjectId('...'),
#           receiver_key_id: "Akfhuio7",
#           message: "...Some message here...",
#           signature: kjasbkfSkdjk83kakj
#       }
#
#   users - Contains documents like:
#       {
#           name: "CoolUsername Lastname"
#           messages_unread: 10
#           keys:
#               {
#                   key_id: "ask38fsk3"
#                   key: "2ptuhwet908weu5hp2c895uc90348[pya58934y5uio43ah..."
#               }
#           ]
#       }

# Set up the proper db connection
MONGOHQ_URL = environ.get("MONGOHQ_URL")
if MONGOHQ_URL:
    mconn = Connection(MONGOHQ_URL)
    db = mconn[urlparse(MONGOHQ_URL).path[1:]]
else:
    mconn = Connection()
    db = mconn.sscs


# Declare the indecies we want mongo to have
indicies = {
        'messages': ['receiver_id'],
        'keys': ['user_id', 'fingerprint'],
        'users': [('username', {'unique': True, 'dropDups': True})]}


# Define a function that uses the indicies above on a mongo database and
# creates them.
def ensure_indices(mdb):
    """Ensures that all of the defined indecies exist."""
    for coll, index_vec in indicies.iteritems():
        for index in index_vec:
            if type(index) == tuple:
                mdb[coll].ensure_index(index[0], **index[1])
            else:
                mdb[coll].ensure_index(index)

# Call the above function.
ensure_indices(db)


def get_user(user, fields=None):
    """Returns a user if one is found in the data store with a matching id."""
    if type(user) == UUID:
        user_doc = db.users.find_one(user, fields=fields)
    else:
        user_doc = db.users.find_one({'username': user}, fields=fields)
    return user_doc


def user_exists(user_id):
    """Returns whether or not the given user_id exists in the database.

    Effectively, this is the complement of get_user."""
    return not None == get_user(user_id, {})


def get_key(key_id):
    """Function to help clients get a key for a specific user."""
    if type(key_id) == UUID:
        return db.keys.find_one(key_id)
    else:
        return db.keys.find_one({'fingerprint': key_id})


def get_user_keys(user_id):
    """Retrives all available keys for a given user."""
    return db.keys.find({'user_id': user_id}, ['key', 'fingerprint'])


def user_has_key(user_id, key_id):
    """Determines whether the given user has the given key or not."""
    return bool(db.keys.find_one({'_id': key_id, 'user_id': user_id}))


def add_message(data):
    """Adds a the given message to the messages collection."""
    return db.messages.insert(data)


def add_user_keys(user_id, keys):
    """Adds the given keys to the keys collection and returns a list of the
    uuids generated for them."""
    return db.keys.insert([{
        '_id': uuid.uuid4(),
        'user_id': user_id,
        'fingerprint': science.key_to_fingerprint(k),
        'key': k} for k in keys])


def add_user(user):
    """Adds the given user to the users collection."""
    # Generates a random uuid for the given user.
    user['_id'] = uuid.uuid4()

    # Replace array of keys with an array of uuids where each uuid references
    # the original key in the keys collection.
    keys = user['keys']
    del user['keys']
    user_uuid = db.users.insert(user, safe=True)
    add_user_keys(user_uuid, keys)
    # Add the user to the database and give the result back to the client.
    return user_uuid


def get_messages(user_id):
    """Gets available messages for the given user_id."""
    return db.messages.find({'receiver_id': user_id})


def remove_messages(msg_ids):
    """Removes each of the given messages from mongo."""
    # TODO: Implement once authentication is.
    pass
