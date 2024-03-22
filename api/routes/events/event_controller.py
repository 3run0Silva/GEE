from flask import Blueprint, jsonify
from .event_service import EventService

event_blueprint = Blueprint('events', __name__)
event_service = EventService()

##################################################################
######################## ROUTES ##################################
##################################################################

# GET ALL EVENTS
@event_blueprint.route('/', methods=['GET'])
def get_events():
  events = event_service.get_all_events()
  return jsonify([event.__dict__ for event in events])

# GET EVENTS BY {TAG}
@event_blueprint.route('/tag/<event_tag>', methods=['GET'])
def get_tag(event_tag):
  events = event_service.get_events_by_tag(event_tag)
  if events:
    return jsonify([event.__dict__ for event in events]), 200 
  else:
    return jsonify({"error": "Event not found"}), 404
  
# GET EVENTS BY {Date}
@event_blueprint.route('/date/<event_date>', methods=['GET'])
def get_date(event_date):
  events = event_service.get_events_by_date(event_date)
  if events:
    return jsonify([event.__dic__ for event in events]), 200 
  else:
    return jsonify({"error": "Event not found"}), 404
  