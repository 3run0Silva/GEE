import os
import firebase_admin
from firebase_admin import firestore, credentials

cred_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cred.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

def get_db():
    return firestore.client()
