import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=False,  
    connect_args={'check_same_thread': False} if 'sqlite' in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal)

Base = declarative_base()
def get_session():
    """Get a database session"""
    return Session()
def init_database():
    """Initialize the database by creating all tables"""
    try:
    
        from models.user import User
        from models.campaign import Campaign
        from models.donation import Donation
        
        Base.metadata.create_all(bind=engine)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
def close_session():
    """Close the current database session"""
    Session.remove()
