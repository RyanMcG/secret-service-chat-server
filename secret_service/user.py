class User(object):
    """A class to help manipulate users."""

    def __init__(self, doc):
        self.doc = doc.decode()
        self.keys = {keyDoc['key_id']: keyDoc['key'] for keyDoc in
                self.doc['keys']}

    def is_active(self):
        return False

    def is_authenticated(self):
        return False

    def get_id(self):
        return self.doc._id

    def has_key(self, key_id):
        return key_id in self.keys
