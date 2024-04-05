from config.database.db import get_db
from .event import Event


##################################################
################# DB ACCESS ######################
##################################################

# FETCH ALL EVENTS
class EventRepository:
  def _fetch_all_events(self):
    db = get_db()
    documents = db.collection('Events').get()
    events = [Event(**doc.to_dict()) for doc in documents]
    return events

  # FETCH EVENTS BY {TAG}
  def _fetch_events_by_tag(self, event_tag):
    db = get_db()
    query = db.collection('Events').where('tag', '==', event_tag).get()
    events = [Event(**doc.to_dict()) for doc in query if doc.exists]
    return events

  # FETCH EVENTS BY {DATE}
  def _fetch_events_by_date(self, day=None, month=None, year=None):
    db = get_db()
    query = db.collection('Events')

    if day:
        query = query.where('day', '==', day)
    if month:
        query = query.where('month', '==', month)
    if year:
        query = query.where('year', '==', year)

    documents = query.get()
    return [Event(**doc.to_dict()) for doc in documents]