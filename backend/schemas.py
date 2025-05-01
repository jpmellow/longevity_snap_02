from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
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
    assessment: Dict[str, Any] = Field(..., description="Assessment data containing health metrics")
    prompt: str = Field(..., description="The prompt to send to the LLM")
    api_key: str = Field(..., description="API key for the LLM service")
    llm_model: str = Field(..., description="Name of the LLM model to use (e.g., 'gpt-4')")

class ChatCoachResponse(BaseModel):
    response: str = Field(..., description="The LLM's response text")

def to_dict(obj):
    """Convert a Pydantic model instance to a dictionary"""
    return obj.dict()
