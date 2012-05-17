from pymongo import Connection
from secret_service import validators as is_valid


mconn = Connection()
db = mconn.sscs


def add_new_message(request):
    if is_valid.new_message(request):
        #db.messages.insert(request.json)
        return request.data
    else:
        return False
