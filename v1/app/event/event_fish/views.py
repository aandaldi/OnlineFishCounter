from flask import Blueprint, make_response, jsonify, request
from datetime import datetime as dt
from app import guard
from app.event.event_fish.models import EventFishModel
from flask_praetorian import auth_required

event_fish_blueprint = Blueprint('event_fish', __name__, url_prefix='/events/<eventId>/customers')


@event_fish_blueprint.route('')
@auth_required
def index(eventId):
    return make_response(jsonify({
        'message': 'This is obtained fish user Event Index'
    }), 200)


@event_fish_blueprint.route('/<customerId>', methods=['POST'])
@auth_required
def add_fish_obtained_by_user(eventId, customerId):
    header = request.headers['Authorization']
    user_id = guard.extract_jwt_token(header.split()[1]).get('id')

    args = request.get_json()

    event_fish = EventFishModel(
        stick_number=args.get('stick_number'),
        fish_weight=args.get('fish_weight'),
        usermanagement_uuid=customerId,
        event_uuid=eventId,
        created_by=user_id,
        date_created=dt.now(),
        modified_by=user_id,
        date_modified=dt.now()
    )

    try:
        event_fish.save_to_db()

        print("POST EVENT_FISH {}".format(event_fish.to_json()))

        return make_response(jsonify({
            'message': 'success add new event fish obtained by user',
            'event_fish': event_fish.to_json()
        }), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "something error"}), 500)


@event_fish_blueprint.route('/<customerId>/<eventFishId>', methods=['GET'])
@auth_required
def get_fish_obtained_by_user_data(eventId, customerId, eventFishId):
    event_fish = EventFishModel.lookup_by_id(eventFishId)

    if event_fish:
        return make_response(jsonify({
            'message': 'success get event fish obtained by user {} on {} event'.format(customerId, eventId),
            'event_fish': event_fish.to_json()
        }), 200)
    else:
        link = '/'
        return make_response(jsonify({
            'message': 'not found event fish id',
            'link': link
        }), 404)


@event_fish_blueprint.route('/<customerId>/<eventFishId>', methods=['PATCH'])
def update_fish_obtained_by_user(eventId, customerId, eventFishId):
    args = request.get_json()

    event_fish = EventFishModel.lookup_by_id(eventFishId)

    if event_fish:
        header = request.headers['Authorization']
        user_id = guard.extract_jwt_token(header.split()[1]).get('id')

        event_fish.stick_number = args.get('stick_number')
        event_fish.fish_weight = args.get('fish_weight')
        event_fish.usermanagement_uuid = customerId
        event_fish.event_uuid = eventId
        event_fish.modified_by = user_id
        event_fish.date_modified = dt.now()

        try:
            event_fish.update_on_db()
            print("PATCH EVENT_FISH {}".format(event_fish.to_json()))
            return make_response(jsonify({
                'message': 'success update event fish obtained by user',
                'event_fish': event_fish.to_json()
            }), 200)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "something error"}), 500)
    else:
        return make_response(jsonify({"message": "event fish obtained by user not found"}), 404)
