from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import User
from schemas.profile import UserProfileResponse

router = APIRouter()

@router.get("/profile/{user_id}", response_model=UserProfileResponse, tags=["Profile"])
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    return user