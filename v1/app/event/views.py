from flask import Blueprint, jsonify, make_response, request
from flask_praetorian import auth_required
from app import swagger, guard
from app.event.models import EventModel
from datetime import datetime as dt

event_blueprint = Blueprint('event', __name__, url_prefix='/events')


@event_blueprint.route('', methods=['GET'])
@auth_required
def index():
    """
    This is Index of Event Page
    ---
    description: This is Index
    tags:
        - Event

    responses:
        200:
            description: index PAGE
    """
    return make_response(jsonify({
        'message': 'This is Event Index'
    }), 200)


@event_blueprint.route('/', methods=['POST'])
@auth_required
def create_event():
    """
        This is Index of Event Page
        ---
        """
    header = request.headers['Authorization']
    user_id = guard.extract_jwt_token(header.split()[1]).get('id')

    args = request.get_json()
    name = args.get('name')
    date = dt.strptime(args.get('date'), '%Y-%m-%d %H:%M:%S')
    max_stick = args.get('max_stick')
    created_by = user_id
    date_created = dt.now()
    modified_by = user_id
    date_modified = dt.now()

    event = EventModel.lookup(name)
    if event:
        return make_response(jsonify({
            'message': 'event already exists'
        }), 400)

    else:
        new_event = EventModel(
            name=name,
            date=date,
            max_stick=max_stick,
            date_created=date_created,
            created_by=created_by,
            date_modified=date_modified,
            modified_by=modified_by
        )
        try:
            new_event.save_to_db()
            print("POST EVENT ", new_event.to_json())
            return make_response(jsonify({
                'message': 'success add new event',
                'event': new_event.to_json()
            }), 201)

        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "something error"}), 500)


@event_blueprint.route('/<eventId>', methods=['GET'])
@auth_required
def get_event_data(eventId):
    """
        This is endpoint for get data event
    :param eventId:
    :return:
    """
    try:
        event = EventModel.lookup_by_id(eventId)
        if event:
            return make_response(jsonify({
                'message': 'success get event data',
                'event': event.to_json()
            }), 200)
        return make_response(jsonify({
            'message': 'event not found',
        }), 404)
    except Exception as e:
        print(e)
        return make_response(jsonify({"message": "something error"}), 500)


@event_blueprint.route('/<eventId>', methods=['PATCH'])
@auth_required
def update_event_data(eventId):
    event = EventModel.lookup_by_id(eventId)

    if event:
        header = request.headers['Authorization']
        user_id = guard.extract_jwt_token(header.split()[1]).get('id')

        args = request.get_json()
        event.name = args.get('name')
        event.date = dt.strptime(args.get('date'), '%Y-%m-%d %H:%M:%S')
        event.max_stick = args.get('max_stick')
        event.modified_by = user_id
        event.date_modified = dt.now()

        try:
            print("PATCH EVENT ", event.to_json())
            return make_response(jsonify({
                'message': 'success update event {}'.format(event.name),
                'event': event.to_json()
            }), 201)

        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "something error"}), 500)
    else:
        return make_response(jsonify({"message": "event not found"}), 404)
