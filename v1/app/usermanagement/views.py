from flask import Blueprint, request, make_response, jsonify
from .models import UsermanagementModel
from datetime import datetime as dt
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
@auth_required
def register_user():
    """
        file: apidocs/register_user.yml
    """
    header = request.headers['Authorization']
    user_id = guard.extract_jwt_token(header.split()[1]).get('id')

    args = request.get_json()

    username = args.get('username')
    password = guard.hash_password(args.get('password'))
    roles = args.get('roles')

    new_user = UsermanagementModel(
        username=username,
        password=password,
        roles=roles,
        created_by=user_id,
        date_modified=dt.now(),
        modified_by=user_id
    )

    try:
        user_db = UsermanagementModel.lookup(username)
        if user_db:
            return make_response(jsonify({"message": "username {} already exists".format(username)}), 400)
        else:
            new_user.save_to_db()
            print("POST USERMANAGEMENT {}".format(new_user.to_json()))
            return make_response(jsonify({"message": "Greattt register {} success".format(username),
                                          "usermanagement": new_user.to_json()}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "something error"}), 500)


@user_blueprint.route("/<username>", methods=['GET'])
@auth_required
def get_user_data(username):
    user = UsermanagementModel.lookup(username)
    if user:
        return make_response(jsonify({"message": "success get data user", "user": user.to_json()}), 200)
    return make_response(jsonify({"message": "user not exists"}), 404)


@user_blueprint.route("/<username>", methods=['PATCH'])
@auth_required
def update_user_data(username):
    args = request.get_json()

    try:
        user = UsermanagementModel.lookup(username)
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
