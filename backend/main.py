from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import crud, models, schemas
from database import SessionLocal, engine
from typing import List

# --- JWT Config ---
SECRET_KEY = "CHANGE_THIS_SECRET_KEY"  # Replace with a secure random key in prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- FastAPI App ---
app = FastAPI()

# --- CORS (allow frontend dev) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, set to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB Table Creation ---
models.Base.metadata.create_all(bind=engine)

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- JWT Helpers ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Auth ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
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
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# --- Routes ---
@app.get("/")
def read_root():
    return {"message": "Longevity Snap Backend API is running!"}

# User registration
@app.post("/users/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    user_obj = schemas.UserCreate(username=user.username, password=hashed_password)
    return crud.create_user(db, user=user_obj)

# User login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# CRUD for Assessments
@app.post("/assessments/", response_model=schemas.Assessment)
def create_assessment(assessment: schemas.AssessmentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_assessment(db, assessment, current_user.id)

@app.get("/assessments/", response_model=List[schemas.Assessment])
def get_assessments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    assessments = db.query(models.Assessment).filter(models.Assessment.user_id == current_user.id).offset(skip).limit(limit).all()
    # Deserialize data field for each assessment
    for a in assessments:
        try:
            a.data = json.loads(a.data)
        except Exception:
            a.data = {}
    return assessments

@app.get("/assessments/{assessment_id}", response_model=schemas.Assessment)
def get_assessment(assessment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id, models.Assessment.user_id == current_user.id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    try:
        assessment.data = json.loads(assessment.data)
    except Exception:
        assessment.data = {}
    return assessment

@app.delete("/assessments/{assessment_id}", response_model=str)
def delete_assessment(assessment_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id, models.Assessment.user_id == current_user.id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    db.delete(assessment)
    db.commit()
    return "Assessment deleted"

# --- LLM Chat Coach Endpoint ---
@app.post("/chat-coach/", response_model=schemas.ChatCoachResponse)
def chat_coach(request: schemas.ChatCoachRequest):
    # Log the incoming request (excluding api_key for security)
    logging.info(f"Chat coach request: model={request.llm_model}, prompt_length={len(request.prompt)}, assessment_keys={list(request.assessment.keys())}")
    try:
        # Here you would call the appropriate LLM API based on request.llm_model and api_key
        # For now, return a stubbed response
        dummy_response = f"[Stub] Model: {request.llm_model}. Prompt: {request.prompt[:40]}... Assessment keys: {list(request.assessment.keys())}"
        return schemas.ChatCoachResponse(response=dummy_response)
    except Exception as e:
        logging.error(f"LLM chat-coach error: {e}")
        raise HTTPException(status_code=500, detail="LLM service error. Please try again later.")
