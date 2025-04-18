import firebase_admin
from firebase_admin import credentials, firestore
from service.config import config

cred = credentials.Certificate(config.firestore_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_record(collection: str, data: dict):
    db.collection(collection).add(data)