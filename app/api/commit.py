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
@router.get("/{user_id}/commit", response_model=List[CommitResponse], tags=["commit"])
def get_commits(user_id: int, commit_id: Optional[int] = None, db: Session = Depends(get_db)):
    commits = get_commit(db, commit_id, user_id)
    
    # 커밋이 없으면 404 반환
    if commit_id and not commits:
        raise HTTPException(status_code=404, detail="Commit not found")
    return commits

# 커밋 수정
@router.put("/{user_id}/commit/{commit_id}", response_model=CommitResponse, tags=["commit"])
def update_commit_info(user_id: int, commit_id: int, commit: CommitCreate, db: Session = Depends(get_db)):
    # commit_id와 user_id를 기반으로 커밋을 찾습니다.
    db_commit = update_commit(db, commit_id, commit, user_id)
    
    # 커밋이 존재하지 않으면 404 오류를 발생시킵니다.
    if not db_commit:
        raise HTTPException(status_code=404, detail="Commit not found")
    
    return db_commit

# 커밋 삭제
@router.delete("/{user_id}/commit/{commit_id}", response_model=CommitResponse, tags=["commit"])
def delete_commit_info(user_id: int, commit_id: int, db: Session = Depends(get_db)):
    commit = delete_commit(db, commit_id, user_id)
    if not commit:
        raise HTTPException(status_code=404, detail="Commit not found")
    return commit
