from .event_repository import fetch_all_events

def get_all_events():
  events = fetch_all_events()
  return events