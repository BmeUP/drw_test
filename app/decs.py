from functools import wraps
from flask import request, Response

def login_required(f):
    """
        simple decorator for check if user login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.authorization is None or\
            request.authorization.get('username') == '' or\
            request.authorization.get('password') == '':
            return Response('Login required', status=403)
        return f(*args, **kwargs)
    return decorated_function