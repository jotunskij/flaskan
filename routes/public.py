from flask import (
    render_template, send_from_directory,
    Blueprint, request, redirect, url_for,
    make_response
)
from flask_jwt_extended import (
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies, jwt_optional,
    get_raw_jwt, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required
)
import requests
import util

public_routes = Blueprint('public_routes', __name__)

@public_routes.route('/static/<path:path>')
def get_js(path):
    return send_from_directory('static', path)

@public_routes.route('/', methods=['GET'])
def index():
    return render_template('public/index.html')

@public_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('public/login.html')
    else:
        next_url = '.index'
        if request.form['next_url']:
            next_url = request.form['next_url']
        api_response = util.api_login()
        response = make_response(redirect(url_for(next_url)))
        for name, value in api_response.cookies.items():
            response.set_cookie(name, value)
        return response

@public_routes.route('/logout', methods=['GET'])
@jwt_optional
def logout():
    util.api_logout((get_raw_jwt() or {}).get("csrf"))
    response = make_response(redirect(url_for('public_routes.logout_refresh')))
    return response

@public_routes.route('/logout-refresh', methods=['GET'])
@jwt_refresh_token_required
def logout_refresh():
    util.api_logout_refresh((get_raw_jwt() or {}).get("csrf"))
    response = make_response(render_template(
        'public/login.html', error='Du är nu utloggad'
    ))
    unset_jwt_cookies(response)
    return response
