from os import environ
from pymongo import Connection
from urlparse import urlparse
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
        'keys': ['fingerprint'],
        'users': ['username']}


# Define a function that uses the indicies above on a mongo database and
# creates them.
def ensure_indices(mdb):
    """Ensures that all of the defined indecies exist."""
    for coll, index_vec in indicies.iteritems():
        for index in index_vec:
            mdb[coll].ensure_index(index)

# Call the above function.
ensure_indices(db)


def get_user(user_id, fields=None):
    """Returns a user if one is found in the data store with a matching id."""
    if fields == None:
        user_doc = db.users.find_one(user_id)
    else:
        user_doc = db.users.find_one(user_id, fields)
    return user_doc


def user_exists(user_id):
    """Returns whether or not the given user_id exists in the database.

    Effectively, this is the complement of get_user."""
    return not None == get_user(user_id, {})


def get_user_key(user_id, key_id=None):
    """Function to help clients get a key for a specific user."""
    if key_id == None:
        return db.users.find({'_id': user_id}, {'keys': 1})['keys']
    else:
        return None


def add_message(data):
    """Adds a the given message to the messages collection."""
    return db.messages.insert(data)


def add_keys(keys):
    """Adds the given keys to the keys collection and returns a list of the
    uuids generated for them."""
    return db.keys.insert([
        {'_id': uuid.uuid4(),
        'fingerprint': science.key_to_fingerprint(k),
        'key': k} for k in keys])


def add_user(user):
    """Adds the given user to the users collection."""
    # Generates a random uuid for the given user.
    user['_id'] = uuid.uuid4()

    # Replace array of keys with an array of uuids where each uuid references
    # the original key in the keys collection.
    user['keys'] = add_keys(user['keys'])

    # Add the user to the database and give the result back to the client.
    return db.users.insert(user)


def get_messages(user_id):
    """Gets available messages for the given user_id."""
    return db.messages.find({'receiver_id': user_id})


def remove_messages(msg_ids):
    """Removes each of the given messages from mongo."""
    # TODO: Implement once authentication is.
    pass
