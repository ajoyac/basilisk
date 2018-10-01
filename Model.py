from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    date_modified = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
    completed = db.relationship('Completed', backref='users', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    def save(self):
        db.session.add(self)
        db.session.commit()


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(1))
    password = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    assessment = db.relationship('Assessment', backref='questions', lazy=True)
    completed = db.relationship('Completed', backref='questions', lazy=True)

    def __init__(self, question):
        self.question = question
        self.assessment = []
    
    def save(self):
        db.session.add(self)
        db.session.commit()


class QuestionSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    question = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()

class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    parameters = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, question_id,parameters,answer):
        self.question_id = question_id
        self.parameters = parameters
        self.answer = answer
    
    def save(self):
        question = Question.query.get(self.question_id)
        question.assessment.append(self)
        db.session.commit()


class AssessmentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    question_id = fields.Integer(required=True)
    parameters  = fields.String(required=True, validate=validate.Length(1))
    answer  = fields.String(required=True, validate=validate.Length(1))
    creation_date = fields.DateTime()
class Completed(db.Model):
    __tablename__ = 'completed'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, question_id,user_id):
        self.question_id = question_id
        self.user_id = user_id

    
    def save(self):
        question = Question.query.get(self.question_id)
        user = User.query.get(self.user_id)
        question.completed.append(self)
        user.completed.append(self)
        db.session.commit()


class CompletedSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    question_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    creation_date = fields.DateTime()