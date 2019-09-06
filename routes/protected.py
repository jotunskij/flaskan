from flask import (
    Blueprint, render_template
)
from flask_jwt_extended import (
    jwt_required
)
from util import group_required_web

protected_routes = Blueprint('protected_routes', __name__)

@protected_routes.route('/protected/user', methods=['GET'])
@jwt_required
@group_required_web(group='user', next_url='protected_routes.user')
def user():
    return render_template('protected/user.html')

@protected_routes.route('/protected/admin', methods=['GET'])
@jwt_required
@group_required_web(group='admin', next_url='protected_routes.admin')
def admin():
    return render_template('protected/admin.html')