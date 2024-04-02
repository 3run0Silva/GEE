from .event_repository import EventRepository

##################################################
################### LOGIC ########################
##################################################
class EventService:

  def __init__(self):
    self.event_repository = EventRepository()

  def get_all_events(self):
    events = self.event_repository._fetch_all_events()
    return events

  def get_events_by_tag(self, event_tag):
    return self.event_repository._fetch_events_by_tag(event_tag)

  def get_events_by_date(self, day=None, month=None, year=None):
    return self.event_repository._fetch_events_by_date(day, month, year)