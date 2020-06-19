from flask import Blueprint, request, make_response, jsonify
from flask_praetorian import Praetorian, auth_required
from app import guard, swagger

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/admins/login', methods=['POST'])
def login_admin():
    """
        file: apidocs/login_admin.yml
    """
    args = request.get_json()
    username = args.get('username')
    password = args.get('password')
    user = guard.authenticate(username, password)
    access_token = guard.encode_jwt_token(user)
    return make_response(jsonify({"message": "login has success",
                                  "access_token": access_token}), 200)


@auth_blueprint.route("/refresh/token", methods=['POST'])
def refresh_token():
    """
        file: apidocs/refresh_token.yml
    """
    print(request.headers['Authorization'])
    args = request.headers['Authorization'].split()
    token = args[1]
    access_token = guard.refresh_jwt_token(token)
    return make_response(jsonify({"message": "refresh has success",
                                  "access_token": access_token}), 200)


@auth_blueprint.route('/logout', methods=['POST'])
# @auth_required
def logout_admin():
    """
    file: apidocs/logout_admin.yml
    """

    return make_response(jsonify({"message": "logout has success",
                                  "link": "/"}), 200)
