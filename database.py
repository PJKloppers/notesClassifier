from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# import PostgresSQL types
# from sqlalchemy.dialects.postgresql import


import os

db_USER = os.environ.get('DB_USER')
db_PASS = os.environ.get('DB_PASSWORD')
db_HOST = os.environ.get('DB_HOST')
db_PORT = os.environ.get('DB_PORT')
db_DATABASE_NAME = os.environ.get('db_DATABASE_NAME')

URL = f'postgresql://{db_USER}:{db_PASS}@{db_HOST}:{db_PORT}/{db_DATABASE_NAME}'
engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
