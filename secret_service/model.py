from pymongo import Connection
from flask import json
from secret_service import validators as is_valid
from secret_service.user import User


mconn = Connection()

# `db` is the mongodb database used by this application. It should have the
# following collections:
#
#   cipthertexts - Contains documents like:
#       {
#           sender_id: ObjectId('...'),
#           sender_key_id: "ask38fsk3"
#           receiver_id: ObjectId('...'),
#           receiver_key_id: "Akfhuio7"
#           ciphertext: "...Some message here..."
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
db = mconn.sscs

indicies = {}
        #'ciphertexts': [
            #{'sender_id': 1},
            #{'receiver_id': 1}]}

def get_req_body(request):
    return request.json if request.json else json(request.body)

def ensure_indices(mdb):
    """Ensures that all of the defined indecies exist."""
    for coll, index_vec in indicies.iteritems():
        for index in index_vec:
            mdb[coll].ensure_index(index)

ensure_indices(db)

def get_user(user_id):
    """Returns a user if one is found in the data store with a matching id."""
    user_doc = db.users.find_one(user_id)
    if user_doc != None:
        return User(user_doc)
    return None

def get_user_key(user_id, key_id=None):
    """Function to help clients get a key for a specific user."""
    if key_id is None:
        pass
    else:
        db.users.find({'_id': user_id})

def add_new_message(data):
    """Adds a the given message to the messages index if it is valid."""
    result = {
            'success': True,
            'data': data}
    (result['success'], errors) =  is_valid.new_message_request(data)
    if (result['success']):
        db.messages.insert(data)
    else:
        result['errors'] = errors
    return result
