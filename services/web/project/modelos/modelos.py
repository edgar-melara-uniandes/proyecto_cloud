from email.policy import default
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from connection_gcp import connect_with_connector
""" from app import db """

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    return connect_with_connector()
    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )
db = None
# init_db lazily instantiates a database connection pool. Users of Cloud Run or
# App Engine may wish to skip this lazy instantiation and connect as soon
# as the function is loaded. This is primarily to help testing.
@app.before_first_request
def init_db() -> sqlalchemy.engine.base.Engine:
    global db
    db = init_connection_pool()
    
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
