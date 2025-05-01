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

from typing import Dict, Any, Optional

class AssessmentBase(BaseModel):
    title: str
    data: Dict[str, Any]

class AssessmentCreate(AssessmentBase):
    pass

class Assessment(AssessmentBase):
    id: int
    created_at: datetime.datetime
    user_id: int
    class Config:
        orm_mode = True

class ChatCoachRequest(BaseModel):
    assessment: Dict[str, Any]
    prompt: str
    api_key: Optional[str] = None
    llm_model: str

class ChatCoachResponse(BaseModel):
    response: str
