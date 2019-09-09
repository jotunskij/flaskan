from functools import wraps
import os
import json
import requests
from flask import redirect, url_for, jsonify
from flask_jwt_extended import (
    get_jwt_identity, verify_jwt_in_request,
    unset_jwt_cookies
)

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

def group_optional_web(group):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                response = redirect_to_login()
                unset_jwt_cookies(response)
                return response
            identity = get_jwt_identity()
            if not identity or group not in identity['groups']:
                return fn(*args, **kwargs)
            else:
                print('Passed')
                kwargs['passed'] = True
                return fn(*args, **kwargs)
        return wrapper
    return decorator

def group_required_web(group, next_url):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                response = redirect_to_login(next_url)
                unset_jwt_cookies(response)
                return response
            identity = get_jwt_identity()
            if group not in identity['groups']:
                return redirect_to_login(next_url)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def redirect_to_login(next_url=None):
    if not next_url:
        next_url = '.index'
    return redirect(url_for(
        'public_routes.login', 
        next_url=next_url,
        error=(
            'Du saknar rättigheter eller har '
            'blivit utloggad pga inaktivitet'
        )
    ))

def log_in_user(username, password):
    # Perform login functionality
    return {'user_id': 1, 'groups': ['admin', 'user']}

def validate_recaptcha(token):
    secret = os.environ.get('RECAPTCHA_SECRET')
    payload = {'response': token, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success']
