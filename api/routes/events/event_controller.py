from flask import Blueprint, jsonify
from .event_service import EventService
from flask import request

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from utils.decorators import error_handler
from execptions.NotFoundException import NotFoundException

event_blueprint = Blueprint('events', __name__)
event_service = EventService()

##################################################################
######################## ROUTES ##################################
##################################################################

# GET ALL EVENTS
@event_blueprint.route('/', methods=['GET'])
@error_handler
def get_events():
  events = event_service.get_all_events()
  if events:
    return jsonify([event.__dict__ for event in events])
  else:
    raise NotFoundException("No events found.")
  
# GET EVENTS BY {TAG}
@event_blueprint.route('/tag/<event_tag>', methods=['GET'])
@error_handler
def get_tag(event_tag):
  events = event_service.get_events_by_tag(event_tag)
  if events:
    return jsonify([event.__dict__ for event in events]), 200 
  else:
    raise NotFoundException("Event not found")
  
# GET EVENTS BY {Date}
@event_blueprint.route('/date', methods=['GET'])
@error_handler
def get_date():
    day = request.args.get('day', default=None, type=int)
    month = request.args.get('month', default=None, type=int)
    year = request.args.get('year', default=None, type=int)
    
    print(f"Day: ({type(day)} : {day}), Month: {month}, Year: {year}")

    events = event_service.get_events_by_date(day=day, month=month, year=year)
    if events:
      return jsonify([event.__dict__ for event in events]), 200 
    else:
      raise NotFoundException("Event not found")