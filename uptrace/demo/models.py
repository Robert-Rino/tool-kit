from demo import db

class User(db.Document):
    username = db.StringField(required=True)
