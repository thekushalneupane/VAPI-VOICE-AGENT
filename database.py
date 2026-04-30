import datetime as dt

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# URL to connect to the SQLite database file
DATABASE_URL = "sqlite:///./appointments_db.db"

# Create the database engine (connection)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory — used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()

# Appointment table definition
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each appointment
    patient_name = Column(String, index=True)           # Name of the patient
    reason = Column(String, index=True)                 # Reason for visit
    start_time = Column(DateTime, index=True)           # Appointment date and time
    canceled = Column(Boolean, default=False)           # Is appointment canceled?
    created_at = Column(DateTime, default=dt.datetime.utcnow)  # When record was created

# Creates all tables in the database if they don't exist
def init_db() -> None:
    Base.metadata.create_all(bind=engine)

init_db()  # Initialize the database when this module is imported