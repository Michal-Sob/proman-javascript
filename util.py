from functools import wraps
from flask import jsonify, session


def json_response(func):
    """
    Converts the returned dictionary into a JSON response
    :param func:
    :return:
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        return jsonify(func(*args, **kwargs))

    return decorated_function


def is_logged_in():
    logged_in = False
    if 'username' in session:
        logged_in = True
    return logged_in


def session_username():
    if 'username' in session:
        return session['username']
    else:
        return None
