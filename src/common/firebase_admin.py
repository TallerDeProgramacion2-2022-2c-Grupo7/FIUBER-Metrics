import os
import json
from base64 import b64decode
import firebase_admin
import firebase_admin.firestore
from firebase_admin import credentials, auth

try:
    _json_str = b64decode(os.environ["FIREBASE_CREDENTIALS"]).decode()
    admin_credentials = json.loads(_json_str)
except KeyError:
    admin_credentials = "firebase_credentials.json"

firebase_credentials = credentials.Certificate(admin_credentials)
firebase_admin.initialize_app(firebase_credentials)
firestore = firebase_admin.firestore.client()
