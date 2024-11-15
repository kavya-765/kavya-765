from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker

# Initialize database
engine = create_engine('sqlite:///users.db')
metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String, unique=True),
              Column('password', String))

metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def add_user(username, password):
    session = Session()
    existing_user = session.query(users).filter_by(username=username).first()
    if existing_user:
        session.close()
        return False  # User already exists
    new_user = users.insert().values(username=username, password=password)
    session.execute(new_user)
    session.commit()
    session.close()
    return True  # User added successfully
