from functools import wraps
from util import group_required_api, log_in_user, TOKEN_BLACKLIST
from flask import (
    request, jsonify, Blueprint
)
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token,
    jwt_refresh_token_required,
    set_access_cookies, set_refresh_cookies,
    get_raw_jwt
)
from flask_cors import cross_origin

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/login', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'],
              supports_credentials=True)
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
    response = jsonify({'loggedIn': True})
    access_token = create_access_token(identity)
    refresh_token = create_refresh_token(identity)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

@api_routes.route('/api/token/refresh', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'],
              supports_credentials=True)
@jwt_refresh_token_required
def api_refresh_token():
    identity = get_jwt_identity()
    response = jsonify({'refreshed': True})
    access_token = create_access_token(identity=identity)
    set_access_cookies(response, access_token)
    return response, 200

# Endpoint for revoking the current users access token
@api_routes.route('/api/logout', methods=['DELETE'])
@cross_origin(headers=['Content-Type', 'Authorization'],
              supports_credentials=True)
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    TOKEN_BLACKLIST.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# Endpoint for revoking the current users refresh token
@api_routes.route('/api/logout-refresh', methods=['DELETE'])
@cross_origin(headers=['Content-Type', 'Authorization'],
              supports_credentials=True)
@jwt_refresh_token_required
def logout_refresh():
    jti = get_raw_jwt()['jti']
    TOKEN_BLACKLIST.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

@api_routes.route('/api/admin', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'],
              supports_credentials=True)
@jwt_required
@group_required_api(group='admin')
def api_admin():
    return jsonify({'data': 'admin'}), 200

@api_routes.route('/api/user', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'],
              supports_credentials=True) 
@jwt_required
def api_user():
    response = jsonify({'data': 'user'})
    return response, 200