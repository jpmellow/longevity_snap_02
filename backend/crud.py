from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

import json

def create_assessment(db: Session, assessment: schemas.AssessmentCreate, user_id: int):
    # Serialize data dict as JSON string for storage
    db_assessment = models.Assessment(
        title=assessment.title,
        data=json.dumps(assessment.data),
        user_id=user_id
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    # Deserialize before returning (optional, for API)
    db_assessment.data = json.loads(db_assessment.data)
    return db_assessment
