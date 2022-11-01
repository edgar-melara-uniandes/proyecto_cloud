from email.policy import default
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app import db
""" db = SQLAlchemy() """

class Appuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    tasks = db.relationship('Task', cascade='all, delete, delete-orphan')
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime, default=datetime.now())
    format_input = db.Column(db.String(50))
    format_output = db.Column(db.String(50))
    path_input = db.Column(db.String(500))
    path_output = db.Column(db.String(500))
    status = db.Column(db.String(50))
    folder = db.Column(db.String(500))
    file_name = db.Column(db.String(50))
    id_user =  db.Column(db.Integer, db.ForeignKey('appuser.id'))
    
    
   
class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
        
class AppuserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Appuser
        include_relationships = True
        load_instance = True
    tasks = fields.List(fields.Nested(TaskSchema()))
