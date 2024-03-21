from flask import Blueprint
from .event_service import get_all_events

event_blueprint = Blueprint('events', __name__)

@event_blueprint.route('/', methods=['GET'])
def get_events():
  return get_all_events()