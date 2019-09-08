from flask import (
    render_template, send_from_directory,
    Blueprint, request, redirect, url_for,
    make_response
)
from flask_jwt_extended import (
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies, jwt_optional,
    get_raw_jwt, get_jwt_identity,
    create_access_token, create_refresh_token
)
import requests

public_routes = Blueprint('public_routes', __name__)

@public_routes.route('/static/<path:path>')
def get_js(path):
    return send_from_directory('static', path)

@public_routes.route('/', methods=['GET'])
def index():
    return render_template('public/index.html')

@public_routes.route('/login', methods=['GET'])
def login():
        return render_template('public/login.html')

@public_routes.route('/logout', methods=['GET'])
def logout():
    response = make_response(render_template('public/login.html'))
    unset_jwt_cookies(response)
    return response
