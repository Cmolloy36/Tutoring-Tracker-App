import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db_url = "sqlite:///tutoring_tracker.db"

file_path = os.path.abspath(__file__)
env_file_path = os.path.abspath(os.path.join(file_path,"..","..",".env"))
load_dotenv(env_file_path)

db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url, echo=False) # Set echo to false for quiet output
SessionLocal = sessionmaker(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()