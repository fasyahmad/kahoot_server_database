import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    tablename = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    email = db.Column(db.String())
    

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self. email =   email

    def __repr__(self):
        return '<user id {}>'.format(self.user_id)
    
    def serialize(self):
        return{
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
