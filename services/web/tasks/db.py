from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.getenv("DATABASE_URL", "sqlite://test.db"))
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()