from pydantic import BaseModel
from typing import Optional, List
import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class AssessmentBase(BaseModel):
    title: str
    data: str

class AssessmentCreate(AssessmentBase):
    pass

class Assessment(AssessmentBase):
    id: int
    created_at: datetime.datetime
    user_id: int
    class Config:
        orm_mode = True
