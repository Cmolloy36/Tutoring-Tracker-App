from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "sqlite:///tutoring_tracker.db"

engine = create_engine(db_url, echo=False) # Set echo to false for quiet output
SessionLocal = sessionmaker(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()