import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db
# db = SQLAlchemy()

# User==================================================
class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    email = db.Column(db.String())
    quiz = db.relationship('Quizzes', cascade='all,delete', backref='users', lazy=True)
    

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self. email = email

    def __repr__(self):
        return '<user id {}>'.format(self.user_id)
    
    def serialize(self):
        return{
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'quiz' : [{'quiz_name':item.quiz_name, 'quiz_category':item.quiz_category } for item in self.quiz]
        }
# =========================================================

# Quizzes =================================================
class Quizzes(db.Model):
    __tablename__ = 'quizzes'

    quiz_id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    quiz_name = db.Column(db.String())
    quiz_category = db.Column(db.String())
    questions = db.relationship('Questions',cascade='all,delete', backref='quizzes', lazy=True) 

    def __init__(self, creator_id, quiz_name, quiz_category):
        self.creator_id = creator_id
        self.quiz_name = quiz_name
        self.quiz_category = quiz_category
    
    def __repr__(self):
        return'<quiz id {}>'.format(self.quiz_id)
    
    def serialize(self):
        return{
            'quiz_id' : self.quiz_id,
            'creator_id' : self.creator_id,
            'quiz_name' : self.quiz_name,
            'quiz_category' : self.quiz_category,
            # 'question_list' : [{'answer':item.answer, 'question':item.question, 'question_number':item.question_number} for item in self.question_list]
        }
# ==========================================================
# Questions ================================================
class Questions(db.Model):
    __tablename__ = "questions"

    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    question_number = db.Column(db.Integer())
    question = db.Column(db.String())
    answer = db.Column(db.String())
    option_list = db.relationship('OptionList', cascade='all,delete', backref='questions', lazy=True)

    def __init__(self, question_id, quiz_id, question_number, question, answer):
        
        self.question_id = question_id
        self.quiz_id = quiz_id
        self.question_number = question_number
        self.question = question
        self.answer = answer
    
    def __repr__(self):
        return'<question id {}>'.format(self.question_id)

    def serialize(self):
        return{
            # 'question_id' : self.question_id,
            'quiz_id' : self.quiz_id,
            'question_id' : self.question_id,
            'question_number' : self.question_number,
            'question' : self.question,
            'answer' : self.answer,
            'option_list' : [{'a':item.a, 'b':item.b, 'c':item.c, 'd':item.d, 'question_id': item.question_id } for item in self.option_list]
        }

# Options List ==============================================
class OptionList(db.Model):
    __tablename__ = "option_list"

    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.question_id'), nullable=False)
    a = db.Column(db.String())
    b = db.Column(db.String())
    c = db.Column(db.String())
    d = db.Column(db.String())

    def __init__(self, option_id, question_id, a, b, c, d):
        self.option_id = option_id
        self.question_id = question_id
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def __repr__(self):
        return'<option id {}>'.format(self.option_id)

    def serialize(self):
        return {
            'option_id' : self.option_id,
            'question_id' : self.question_id,
            'a' : self.a,
            'b' : self.b,
            'c' : self.c,
            'd' : self.d
        }
# ===========================================================

#  Game =====================================================
class Game(db.Model):
    __tablename__ = 'game'

    game_pin = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id'), nullable=False)
    quizzes = db.relationship('Quizzes', cascade='all,delete', backref='game', lazy=True)

 

    def __init__(self, game_pin, quiz_id):
        self.game_pin = game_pin
        self.quiz_id = quiz_id

    def __repr__(self):
        return'<game pin {}>'.format(self.game_pin)

    def serialize(self):
        return {
            'game_pin' : self.game_pin,
            'quiz_id' : self.quiz_id,
            # 'quiz' : [{'quiz_name':item.quiz_name, 'quiz_category':item.quiz_category } for item in self.quiz]
        }

# Leaderboard =================================================
class Leaderboard(db.Model):
    __tablename__ = "leaderboard"
    game_pin = db.Column(db.Integer())
    score = db.Column(db.Integer())
    player_name = db.Column(db.String, primary_key=True)

    def __init__(self, game_pin, score, player_name):
        self.game_pin = game_pin
        self.score = score
        self.player_name = player_name

    def __repr__(self):
        return'<player name {}>'.format(self.player_name)

    def serialize(self):
        return {
            'game_pin' : self.game_pin,
            'score' : self.score,
            'player_name' : self.player_name
    } 