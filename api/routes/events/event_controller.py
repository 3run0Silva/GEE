from flask import Blueprint, jsonify
from .event_service import EventService
from flask import request

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
@event_blueprint.route('/date', methods=['GET'])
def get_date():
    day = request.args.get('day', default=None, type=int)
    month = request.args.get('month', default=None, type=int)
    year = request.args.get('year', default=None, type=int)
    
    print(f"Day: {day}, Month: {month}, Year: {year}")

    events = event_service.get_events_by_date(day=day, month=month, year=year)
    if events:
      return jsonify([event.__dict__ for event in events]), 200 
    else:
      return jsonify({"error": "Event not found"}), 404
    