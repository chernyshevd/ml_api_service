"""
Module for the machine learning API service.
"""
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt

import config
from ml.ml import get_ml_service
from models.models import InputData, User
from db.db import get_db, UserDB, create_initial_users

app = FastAPI()

# Конфигурация JWT
SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup_event():
    """Initializes the database and creates initial users."""
    db = next(get_db())
    create_initial_users(db)

@app.on_event("shutdown")
async def shutdown_event():
    """Handles cleanup tasks on shutdown."""
    pass

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

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Issues a JWT token for authentication."""
    db = next(get_db())
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

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

def role_required(role: str):
    """Decorator to enforce role-based access control."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            user = await get_current_user()  # Получаем текущего пользователя
            if user.role != role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Доступ запрещен"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@app.post("/model_fit")
@role_required("admin")
async def model_fit(user: User = Depends(get_current_user)):
    """Trains and saves the machine learning model."""
    try:
        model = get_ml_service(config.BASE_DIR)
        model.create_model()
        return {"message": "Model successfully trained and saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict(data: InputData, user: User = Depends(get_current_user)):
    """Makes a prediction based on input data."""
    model = get_ml_service(config.BASE_DIR)
    features = [[data.feature1, data.feature2, data.feature3, data.feature4]]
    prediction = model.predict(features)
    prediction = prediction.tolist()
    return {"prediction": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
