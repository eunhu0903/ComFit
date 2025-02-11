from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.token import verify_token
from models.user import User
from db.session import get_db

router = APIRouter()

@router.get("/home")
def home(token: str, db: Session = Depends(get_db)):
    email = verify_token(token, db)
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    
    username = user.username
    return {"message": f"{username}님, 환영합니다!"}


