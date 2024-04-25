from functools import wraps
from flask import request, abort
import os, jwt

def require_basic_auth(api_method):
    @wraps(api_method)

    def check_basic_auth(*args, **kwargs):
        auth_object = request.authorization
        if auth_object and auth_object.username and auth_object.password:
            kwargs['user'] = {auth_object.username: auth_object.password}
            return api_method(*args, **kwargs)
        else:
            abort(401)

    return check_basic_auth

def require_jwt_token(api_method):
    @wraps(api_method)

    def check_jwt_token(*args, **kwargs):
        
        secret = os.getenv('JWT_SECRET')
        if not secret:
            abort(401)
        
        bearer = request.headers.get('Authorization') 
        
        if not bearer:
          abort(401)
        
        token = bearer.split()[1]  
        
        decoded_jwt = jwt.decode(token, secret, algorithms=["HS256"])
        if token and decoded_jwt['email']:
            kwargs['user'] = decoded_jwt['email']
            return api_method(*args, **kwargs)
        else:
            abort(403)

    return check_jwt_token