from flask import (
    Blueprint, render_template
)
from flask_jwt_extended import (
    jwt_optional
)
from util import group_required_web, group_optional_web

protected_routes = Blueprint('protected_routes', __name__)

@protected_routes.route('/protected/user', methods=['GET'])
@group_required_web(group='user', next_url='/protected/user')
def user():
    print(f'Rendering /protected/user')
    return render_template('protected/user.html')

@protected_routes.route('/protected/admin', methods=['GET'])
@group_required_web(group='admin', next_url='/protected/admin')
def admin():
    print(f'Rendering /protected/admin')
    return render_template('protected/admin.html')

@protected_routes.route('/protected/dynamic', methods=['GET'])
@group_optional_web(group='admin')
def dynamic(passed=False):
    if passed:
        return render_template('protected/admin.html')
    else:
        return render_template('protected/user.html')
    # Or send a template variable
    # render_template('protected/or_not.html, is_admin=passed)