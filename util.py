from functools import wraps
import os
import json
import requests
from flask import redirect, request, url_for, jsonify
from flask_jwt_extended import get_jwt_identity

# Decorators
def group_required_api(group):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if group not in identity['groups']:
                return jsonify({'error': 'Token doesnt have the correct group'}), 400
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def group_required_web(group, next_url):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            print(f'Identity is: {identity}')
            if group not in identity['groups']:
                print(f'Bad groups -> redirecting to login')
                return redirect(url_for(
                    'public_routes.login_get', 
                    next_url=next_url,
                    error='Du saknar rättigheter'
                ))
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def log_in_user(username, password):
    # Perform login functionality
    # return {'user_id': 1, 'groups': ['admin']}
    return {'user_id': 1, 'groups': ['admin', 'user']}

def validate_recaptcha(token):
    secret = os.environ.get('RECAPTCHA_SECRET')
    payload = {'response': token, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']
