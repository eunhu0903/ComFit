from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.token import get_token_from_header, verify_token
from models.user import User
from models.commit import Commit
from db.session import get_db

router = APIRouter()

@router.get("/{username}", tags=["profile"])
def get_profile(username: str, authorization: str = Depends(get_token_from_header), db: Session = Depends(get_db)):
    verify_token(authorization, db)
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    commit = db.query(Commit).filter(Commit.user_id == user.id).all()
    
    return {
        "username": user.username,
        "commits": commit
        }
