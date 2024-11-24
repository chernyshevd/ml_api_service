"""
Module for the machine learning API service.
"""
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import config
from ml.ml import get_ml_service
from models.models import InputData, User
from db.db import get_db, UserDB, create_initial_users

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Initializes the database and creates initial users."""
    db = next(get_db())
    create_initial_users(db)

@app.on_event("shutdown")
async def shutdown_event():
    """Handles cleanup tasks on shutdown."""
    pass

async def authenticate_user(user: User, db: Session = Depends(get_db)):
    """Authenticates a user by checking username and password."""
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if db_user and db_user.password == user.password:
        return user
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.post("/login")
async def login(user: User, db: Session = Depends(get_db)):
    """Handles user login and returns a success message."""
    await authenticate_user(user, db)
    return {"message": "Authentication successful"}

@app.post("/model_fit")
async def model_fit(user: User = Depends(authenticate_user)):
    """Trains and saves the machine learning model."""
    try:
        model = get_ml_service(config.BASE_DIR)
        model.create_model()
        return {"message": "Model successfully trained and saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict(data: InputData, user: User = Depends(authenticate_user)):
    """Makes a prediction based on input data."""
    model = get_ml_service(config.BASE_DIR)
    features = [[data.feature1, data.feature2, data.feature3, data.feature4]]
    prediction = model.predict(features)
    prediction = prediction.tolist()
    return {"prediction": prediction}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
