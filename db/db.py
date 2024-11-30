"""
Module for setting up the database and defining models.
"""
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Настройка базы данных
DATABASE_URL = "sqlite:///./test.db"  # Путь к вашей базе данных
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Определение модели пользователя
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Пароль хранится в открытом виде
    role = Column(String)  # Добавлено поле для роли

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
def create_initial_users(db: Session):
    admin_user = UserDB(username="admin", password="admin_password", role="admin")
    regular_user = UserDB(username="user", password="user_password", role="user")
    db.add(admin_user)
    db.add(regular_user)
    db.commit()
