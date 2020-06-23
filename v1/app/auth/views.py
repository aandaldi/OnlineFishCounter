import jwt

from flask import Blueprint, request, make_response, jsonify
from flask_praetorian import Praetorian, auth_required
from app import guard, swagger
from .user_session_models import UserSessionModel

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

    try:
        access_token = guard.encode_jwt_token(user)
        usermanagement_uuid = guard.extract_jwt_token(access_token).get('id')

        user_session_db = UserSessionModel.lookup(usermanagement_uuid)
        if user_session_db:
            user_session_db.delete_from_db()

        user_session = UserSessionModel(
            access_token=access_token,
            usermanagement_uuid=usermanagement_uuid
        )
        user_session.save_to_db()

        return make_response(jsonify({"message": "login has success",
                                      "access_token": access_token}), 200)

    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "something error"}), 500)


@auth_blueprint.route("/refresh/token", methods=['POST'])
def refresh_token():
    """
        file: apidocs/refresh_token.yml
    """
    args = request.headers['Authorization'].split()
    token = args[1]
    print(token)
    access_token = guard.refresh_jwt_token(token)
    return make_response(jsonify({"message": "refresh has success",
                                  "access_token": access_token}), 200)


@auth_blueprint.route('/logout', methods=['POST'])
@auth_required
def logout_admin():
    """
    file: apidocs/logout_admin.yml
    """

    args = request.headers['Authorization'].split()
    token = args[1]

    usermanagement_uuid = guard.extract_jwt_token(token).get('id')

    user_session_db = UserSessionModel.lookup(usermanagement_uuid)

    if user_session_db:
        user_session_db.delete_from_db()
    return make_response(jsonify({"message": "logout has success",
                                  "link": "/"}), 200)
