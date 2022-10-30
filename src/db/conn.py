from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "postgresql://postgres:admin@localhost:5432/postgres"
engine = create_engine(DB_URL)
Session = sessionmaker(engine)
Base = declarative_base()
