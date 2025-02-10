from sqlalchemy.orm import Session
from models.commit import Commit
from schemas.commit import CommitCreate
from typing import Optional

def create_commit(db: Session, commit: CommitCreate, user_id: int):
    db_commit = Commit(
        exercise_type=commit.type,
        duration=commit.duration,
        sets=commit.sets,
        intensity=commit.intensity,
        memo=commit.memo,
        user_id=user_id
    )
     
    db.add(db_commit)
    db.commit()
    db.refresh(db_commit)
    return db_commit

def get_commit(db: Session, commit_id: Optional[int] = None, user_id: int = None):
    if commit_id:
        return db.query(Commit).filter(Commit.id == commit_id, Commit.user_id == user_id).first()
    return db.query(Commit)

def update_commit(db: Session, commit_id: int, commit: CommitCreate, user_id: int):
    db_commit = db.query(Commit).filter(Commit.id == commit_id, Commit.user_id == user_id).first()
    if db_commit:
        for key, value in commit.dict().items():
            if value is not None:
                setattr(db_commit, key, value)
            
        db.commit()
        db.refresh(db_commit)
    return db_commit

def delete_commit(db: Session, commit_id: int, user_id: int):
    db_commit = db.query(Commit).filter(Commit.id == commit_id, Commit.user_id == user_id).first()
    if db_commit:
        db.delete(db_commit)
        db.commit()
    return db_commit