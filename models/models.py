"""
Module for defining data models using Pydantic.
"""
from pydantic import BaseModel

class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float

class User(BaseModel):
    username: str
    password: str
    