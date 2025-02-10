from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from db.session import get_db
from schemas.commit import CommitCreate, CommitResponse
from crud.commit import create_commit, get_commit, update_commit, delete_commit

router = APIRouter()

# 커밋 생성
@router.post("/{user_id}/commit", response_model=CommitResponse, tags=["commit"])
def create_new_commit(user_id: int, commit: CommitCreate, db: Session = Depends(get_db)):
    return create_commit(db, commit, user_id)

# 커밋 조회
@router.get("/{user_id}/commit/{user_commit_id}", response_model=CommitResponse, tags=["commit"])
def get_commit_by_user(user_id: int, user_commit_id: int, db: Session = Depends(get_db)):
    commit = get_commit(db, user_id=user_id, user_commit_id=user_commit_id)
    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")
    return commit

# 커밋 수정
@router.put("/{user_id}/commit/{user_commit_id}", response_model=CommitResponse, tags=["commit"])
def update_commit_by_user_commit_id(user_id: int, user_commit_id: int, commit: CommitCreate, db: Session = Depends(get_db)):
    updated_commit = update_commit(db, user_id, user_commit_id, commit)
    if not updated_commit:
        raise HTTPException(status_code=404, detail="Commit not found")
    return updated_commit

# 커밋 삭제
@router.delete("/{user_id}/commit/{user_commit_id}", response_model=CommitResponse, tags=["commit"])
def delete_commit_by_user_commit_id(user_id: int, user_commit_id: int, db: Session = Depends(get_db)):
    deleted_commit = delete_commit(db, user_id, user_commit_id)
    if not deleted_commit:
        raise HTTPException(status_code=404, detail="Commit not found")
    return deleted_commit

