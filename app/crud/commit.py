from sqlalchemy.orm import Session
from models.commit import Commit
from schemas.commit import CommitCreate
from typing import Optional

def create_commit(db: Session, commit: CommitCreate, user_id: int):
    max_user_commit_id = db.query(Commit).filter(Commit.user_id == user_id).order_by(Commit.user_commit_id.desc()).first()
    if not max_user_commit_id:
        new_user_commit_id = 1
    else:
        new_user_commit_id = max_user_commit_id.user_commit_id + 1
    
    db_commit = Commit(
        user_commit_id=new_user_commit_id,
        type=commit.type,
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

def get_commit(db: Session, user_id: int, user_commit_id: int):
    return db.query(Commit).filter(Commit.user_id == user_id, Commit.user_commit_id == user_commit_id).first()

def update_commit(db: Session, user_id: int, user_commit_id: int, commit: CommitCreate):
    db_commit = db.query(Commit).filter(Commit.user_id == user_id, Commit.user_commit_id == user_commit_id).first()

    if db_commit:
        for key, value in commit.dict().items():
            if value is not None:
                setattr(db_commit, key, value)

        db.commit()
        db.refresh(db_commit)
        return db_commit
    return None

def delete_commit(db: Session, user_id: int, user_commit_id: int):
    db_commit = db.query(Commit).filter(Commit.user_id == user_id, Commit.user_commit_id == user_commit_id).first()

    if db_commit:
        db.delete(db_commit)
        db.commit()

        commits = db.query(Commit).filter(Commit.user_id == user_id).order_by(Commit.user_commit_id).all()

        for idx, commit in enumerate(commits, start=1):
            commit.user_commit_id = idx

        db.commit()
        return db_commit

    return None

