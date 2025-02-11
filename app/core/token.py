from fastapi import HTTPException, status, Header
from datetime import datetime
from sqlalchemy.orm import Session
from models.user import User
from core.security import decode_access_token

def get_token_from_header(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization token is missing or invalid")
    
    token = authorization[7:]
    return token

def verify_token(token: str, db: Session) -> str:
    try:
        payload = decode_access_token(token)

        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has no email",
            )

        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or token",
            )
        
        expiration: int = payload.get("exp")
        if expiration and expiration < int(datetime.utcnow().timestamp()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )

        return email

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
