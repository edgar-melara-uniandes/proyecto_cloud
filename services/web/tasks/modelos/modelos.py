from datetime import datetime

import tasks.db as db
from sqlalchemy import Column, Integer, String, DateTime

    
class Task(db.Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=datetime.now())
    date_updated = Column(DateTime, default=datetime.now())
    format_input = Column(String(50))
    format_output = Column(String(50))
    path_input = Column(String(500))
    path_output = Column(String(500))
    status = Column(String(50))
    folder = Column(String(500))
    file_name = Column(String(50))
    id_user =  Column(Integer)

    def __init__(self, date_created, date_updated, format_input, format_output, path_input, path_output, status, folder, file_name, id_user):
        self.date_created = date_created
        self.date_updated = date_updated
        self.format_input = format_input
        self.format_output = format_output
        self.path_input = path_input
        self.path_output = path_output
        self.status = status
        self.folder = folder
        self.file_name = file_name
        self.id_user = id_user

    def __repr__(self):
        return f'Task({self.id}, {self.file_name})'

    def __str__(self):
        return self.file_name

