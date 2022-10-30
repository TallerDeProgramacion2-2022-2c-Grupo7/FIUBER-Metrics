import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)
Base = declarative_base()
