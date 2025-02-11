from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from core.token import verify_token
from models.user import User
from models.commit import Commit
from db.session import get_db
from core.token import get_token_from_header


router = APIRouter()

@router.get("/home")
def home(authorization: str = Depends(get_token_from_header), query: str = Query(None, min_length=1), db: Session = Depends(get_db)):
    email = verify_token(authorization, db)
    
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=401,detail="User not found")
    
    welcome_message = f"{user.username}님, 환영합니다!"

    top_committers = (
        db.query(User.username, func.count(Commit.id).label("commit_count"))
        .join(Commit, User.id == Commit.user_id)
        .group_by(User.username)
        .order_by(func.count(Commit.id).desc())
        .limit(5)
        .all()
    )

    if query:
        users = db.query(User).filter(User.username.ilike(f"%{query}%")).all()
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return {
            "users": [{"username": u.username} for u in users]
        }

    return {
        "message": welcome_message,
        "top_committers": [{"username": u, "commit_count": c} for u, c in top_committers],
    }


