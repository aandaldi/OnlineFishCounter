from flask import Blueprint, request, make_response, jsonify
from .models import UserModel
from datetime import datetime
from flask_praetorian import auth_required

from app import guard, swagger

user_blueprint = Blueprint('user', __name__, url_prefix='/users')

@user_blueprint.route("/")
def index():
    """
    file: apidocs/index.yml
    """
    return "hello user"


@user_blueprint.route("", methods=['POST'])
# @auth_required
def register_user():
    """
        file: apidocs/register_user.yml
    """
    args = request.get_json()

    username = args.get('username')
    password = guard.hash_password(args.get('password'))
    roles = args.get('roles')
    created_by = args.get('username')
    modified_date = datetime.utcnow()
    modified_by = args.get('username')

    new_user = UserModel(username, password, roles, created_by, modified_date, modified_by)

    try:
        user_db = UserModel.lookup(username)
        if user_db:
            return make_response(jsonify({"message": "username {} already exists".format(username)}), 409)
        else:
            new_user.save_to_db()
            print("POST {}".format(new_user.to_json()))
            return make_response(jsonify({"message": "Greattt register {} success".format(username)}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "something error"}), 500)


@user_blueprint.route("/<username>", methods=['GET'])
@auth_required
def get_user_data(username):
    try:
        user = UserModel.lookup(username)
        if user:
            return make_response(jsonify({"message": "success get data", "user": user.to_json()}), 200)
        return make_response(jsonify({"message": "user not exists"}), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "something error"}), 500)


@user_blueprint.route("/<username>", methods=['PATCH'])
@auth_required
def update_user_data(username):
    args = request.get_json()

    try:
        user = UserModel.lookup(username)
        if user:
            user.username = args.get('username')
            user.password = args.get('password')
            user.roles = args.get('roles')
            user.created_by = args.get('created_by')
            user.modified_date = datetime.utcnow()
            user.modified_by = args.get('username')

            user.update_on_db()
            print("PATCH {}".format(user.to_json()))

            return make_response(jsonify({"message": "success update data", "user": user.to_json()}), 200)
        return make_response(jsonify({"message": "user not exists"}), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "something error"}), 500)
