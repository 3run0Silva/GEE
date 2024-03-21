from config.database.db import get_db

def fetch_all_events():
  db = get_db()
  events = db.collection('events').get()
  return events