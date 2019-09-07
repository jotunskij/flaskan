import os
import requests
from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from routes.protected import protected_routes
from routes.api import api_routes
from routes.public import public_routes

#
# FLASK SETUP
#

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.environ.get('SECRET_KEY')
app.register_blueprint(protected_routes)
app.register_blueprint(api_routes)
app.register_blueprint(public_routes)

#
# JWT SETUP
#

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = app.secret_key
# Short expiration to demo refresh tokens
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 300
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'user_id': identity['user_id'],
        'groups': identity['groups']
    }

@jwt.expired_token_loader
def token_expired_callback(expired_token):
    return redirect(url_for(
        'public_routes.login_get',
        next_url='/',
        error='Din token har blivit gammal. Logga in på nytt.'
    ))

@app.before_first_request
def initialize():
    # Perform startup initialization here
    pass
