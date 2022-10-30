import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "admin")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_URL = f"postgresql://postgres:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)
Base = declarative_base()
