import os
import requests
import util
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
app.register_blueprint(api_routes)

#
# JWT SETUP
#

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = app.secret_key
# Short expiration to demo refresh tokens
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 10
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'user_id': identity['user_id'],
        'groups': identity['groups']
    }

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in util.TOKEN_BLACKLIST

@app.before_first_request
def initialize():
    # Perform startup initialization here
    pass
