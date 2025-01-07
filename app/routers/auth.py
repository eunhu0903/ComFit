from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import create_access_token, verify_password, get_password_hash
from db.database import get_db
from db.models import User
from schemas.auth import UserCreate, UserResponse, UserLogin

router = APIRouter()

@router.post("/signup", response_model=UserResponse, tags=["Auth"])
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email or User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user