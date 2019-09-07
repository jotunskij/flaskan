from flask import (
    render_template, send_from_directory,
    Blueprint, request, redirect, url_for,
    make_response
)
from flask_jwt_extended import (
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
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
def login_get():
    return render_template('public/login.html')

"""
@public_routes.route('/login', methods=['POST'])
def login_post():
    next_url = request.args.get('next_url')
    if not next_url:
        next_url = '.index'

    recaptcha_token = request.form['g-recaptcha-response']
    # Uncomment to run recaptcha
    # success = util.validate_recaptcha(recaptcha_token)
    success = True
    if not success:
        response = redirect(url_for('.login_get',
            error='Recaptcha failed', 
            next_url=next_url)
        )
        return response    

    username = request.form['username']
    password = request.form['password']

    login_json = {
        'username': username,
        'password': password
    }
    api_url = f'{request.url_root}api/login'
    login_response = requests.post(api_url, json=login_json)
    if login_response.status_code != 200:
        response = redirect(url_for('.login_get',
            error=login_response.text, 
            next_url=next_url)
        )
        return response

    response = redirect(url_for(next_url))
    
    set_access_cookies(response, login_response.json()['access_token'])
    set_refresh_cookies(response, login_response.json()['refresh_token'])
    return response
"""

@public_routes.route('/logout', methods=['GET'])
def logout():
    response = make_response(render_template('public/logout.html'))
    unset_jwt_cookies(response)
    return render_template('public/logout.html')
