from flask import Markup, Response, json
from uuid import UUID
from bson import json_util


def jsonit(data):
    """Similar to jsonify, but includes some mongo niceness."""
    return Response(json.dumps(data, default=json_util.default),
            mimetype='application/json')


def to_uuid(uuid_str):
    """Takes a string and turns it into """
    try:
        return UUID(uuid_str)
    except ValueError:
        return False


def debug_str(print_me):
    """Prints out an HTML escaped string in code and pre tags."""
    if isinstance(print_me, (list, tuple)):
        print_me = "\n".join([str(x) for x in print_me])
    if isinstance(print_me, dict):
        print_me = "{\n\t"
        + "\n\t".join([str(x) + ": " + str(y) for x, y in print_me.items()])
        + "\n}"
    escaped = Markup.escape(str(print_me))
    return """<code class="debug-str"><pre>{0}</pre></code>""".format(escaped)


def str_to_digits(wannabe_number):
    """Returns an integer version of the given string or int by removing all
    non-digit characters."""
    if isinstance(wannabe_number, int):
        return wannabe_number
    else:
        ret = ''.join(filter(lambda x: x.isdigit(), str(wannabe_number)))
        return int(ret) if ret != '' else None


def describe_request(request):
    """Creates a helpful string to descirbe the given request."""
    return str((request.url, request.method, request.headers['Content-Type'],
            request.json if request.json else request.data))
