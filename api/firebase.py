import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebaseConfig.json")

firebase_admin.initialize_app(
    cred,
    {
        "storageBucket": "gokag-19eac.appspot.com",
    },
)
