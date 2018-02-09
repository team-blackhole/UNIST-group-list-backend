from functools import wraps

from flask import g, request 
from flask_restplus import Namespace

from app.auth.models import User

ns = Namespace('Decorators', description='Decorators')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', 'Null')
        # token = [item.encode('ascii') for item in auth_header.split(' ')]
        token = auth_header
        # user = User.verify_auth_token(token) 
        # if len(token) == 2 and token[0] == b'Token':
        user = User.verify_auth_token(token)
        if user:
            g.user = user
            return f(*args, **kwargs)
        ns.abort(401, message='Invalid Token - Authorization Required')

    return decorated_function


def has_permissions(perms=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = g.user
            for p in perms:
                if not user.has_permission(p):
                    ns.abort(401, message='Operation not permitted')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

