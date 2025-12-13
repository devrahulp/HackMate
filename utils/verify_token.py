# utils/verify_token.py
import firebase_admin
from firebase_admin import credentials, auth
import os

SERVICE_KEY = os.path.join(os.path.dirname(__file__), '..', 'serviceAccountKey.json')

if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_KEY)
    firebase_admin.initialize_app(cred)

def verify_id_token(id_token):
    """
    Verifies the Firebase ID token (server side).
    Returns the decoded token (dict) if valid, otherwise raises an exception.
    """
    decoded = auth.verify_id_token(id_token)
    return decoded
