import os
import firebase_admin
from firebase_admin import firestore, credentials

def get_db():
  current_dir = os.path.dirname(os.path.abspath(__file__))
  cred_path = os.path.join(current_dir, 'cred.json')

  cred = credentials.Certificate(cred_path)
  firebase_admin.initialize_app(cred)

  db = firestore.client()

  print(db)

  return firestore.client()