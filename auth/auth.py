from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from db.db import get_db, UserDB

SECRET_KEY = "123456"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(username: str, password: str, db: Session):
    """Authenticates a user by username and password."""
    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if db_user and db_user.password == password:
        return db_user
    return False

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)):
    """Retrieves the current user based on the provided token, raises HTTPException if invalid."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = db.query(UserDB).filter(UserDB.username == username).first()
    if db_user is None:
        raise credentials_exception
    return db_user 