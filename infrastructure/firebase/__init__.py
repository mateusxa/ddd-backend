import firebase_admin
from firebase_admin import credentials


class Firebase:
    
    firebase_admin.initialize_app(
        credentials.Certificate("utils/credentials.json"), 
        {"storageBucket": "xpa-engenharia.appspot.com"},
    )
