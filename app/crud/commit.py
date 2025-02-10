from sqlalchemy.orm import Session
from models.commit import Commit
from schemas.commit import CommitCreate
from typing import Optional

def create_commit(db: Session, commit: CommitCreate, user_id: int):
    db_commit = Commit(
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

def get_commit(db: Session, commit_id: Optional[int] = None, user_id: int = None):
    if commit_id:
        return db.query(Commit).filter(Commit.id == commit_id, Commit.user_id == user_id).first()
    return db.query(Commit)

def update_commit(db: Session, commit_id: int, commit: CommitCreate, user_id: int):
    # commit_id와 user_id로 커밋을 찾습니다.
    db_commit = db.query(Commit).filter(Commit.id == commit_id, Commit.user_id == user_id).first()
    
    if db_commit:
        # 커밋이 존재하면, 전달된 commit 정보로 수정합니다.
        for key, value in commit.dict().items():
            if value is not None:
                setattr(db_commit, key, value)
        
        # 변경 사항을 DB에 반영합니다.
        db.commit()
        db.refresh(db_commit)
        return db_commit
    
    return None  # 커밋이 존재하지 않으면 None 반환

def delete_commit(db: Session, commit_id: int, user_id: int):
    db_commit = db.query(Commit).filter(Commit.id == commit_id, Commit.user_id == user_id).first()
    if db_commit:
        db.delete(db_commit)
        db.commit()
    return db_commit