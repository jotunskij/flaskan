from functools import wraps
from util import group_required_api, log_in_user
from flask import (
    request, jsonify, Blueprint
)
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token,
    jwt_refresh_token_required,
    set_access_cookies, set_refresh_cookies
)

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"error": "Missing username parameter"}), 400
    if not password:
        return jsonify({"error": "Missing password parameter"}), 400

    user = log_in_user(username, password)
    if not user:
        return jsonify({"error": f"Bad username and/or password"}), 400
    identity = {
        'user_id': user['user_id'],
        'groups': user['groups']
    } 
    access_token = create_access_token(identity)
    refresh_token = create_refresh_token(identity)
    response = jsonify(access_token=access_token, refresh_token=refresh_token)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

@api_routes.route('/api/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def api_refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    response = jsonify(access_token=access_token)
    set_access_cookies(response, access_token)
    return response, 200

@api_routes.route('/api/admin', methods=['GET'])
@jwt_required
@group_required_api(group='admin')
def api_admin():
    return jsonify({'data': 'admin'}), 200

@api_routes.route('/api/user', methods=['GET'])
@jwt_required
def api_user():
    return jsonify({'data': 'user'}), 200