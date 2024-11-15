# db.py

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

# Initialize the SQLAlchemy engine and metadata
DATABASE_URL = 'sqlite:///users.db'
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the users table
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String, unique=True),
              Column('password', String))

# Create all tables
metadata.create_all(engine)

# Session maker
Session = sessionmaker(bind=engine)

# Utility function to create a new session
def get_session():
    return Session()

