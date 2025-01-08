from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User
from schemas.profile import UserProfileResponse, UserProfileUpdate

router = APIRouter()

@router.get("/{username}", response_model=UserProfileResponse, tags=["Profile"])
def get_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user

@router.put("/{username}", response_model=UserProfileResponse, tags=["Profile"])
def put_profile(username: str, profile_data: UserProfileUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    
    if profile_data.username:
        user.username = profile_data.username
    else:
        raise HTTPException(status_code=400, detail="Username is required")
    
    db.commit()
    db.refresh(user)
    return user