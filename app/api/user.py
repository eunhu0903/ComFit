from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import create_access_token, verify_password, get_password_hash
from db.session import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter()

@router.post("/signup", response_model=UserResponse, tags=["User"])
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    existing_user = db.query(User).filter(User.email == user.email).first()  
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token, tags=["User"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "Bearer"}