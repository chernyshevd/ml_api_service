"""
Module for setting up the database and defining models.
"""
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка базы данных
DATABASE_URL = "sqlite:///./test.db"  # Путь к вашей базе данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели пользователя
class UserDB(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    password = Column(String)  # Пароль хранится в открытом виде

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Вставка пользователей в базу данных (это можно сделать один раз при инициализации)
def create_initial_users(db):
    users = [
        UserDB(username="user1", password="password1"),  # Пароль в открытом виде
        UserDB(username="user2", password="password2"),  # Пароль в открытом виде
    ]

    for user in users:
        if not db.query(UserDB).filter(UserDB.username == user.username).first():
            db.add(user)
 
    db.commit()
