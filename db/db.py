"""
Module for setting up the database and defining models.
"""
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///./test.db"  # Путь к вашей базе данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    """User model for the database with id, username, password, and role fields."""

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    """Generator function to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_initial_users(db: Session):
    """Create initial users in the database."""
    admin_user = UserDB(username="admin", password="admin_password", role="admin")
    regular_user = UserDB(username="user", password="user_password", role="user")
    db.add(admin_user)
    db.add(regular_user)
    db.commit()
