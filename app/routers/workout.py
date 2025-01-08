from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Workout, User
from schemas.workout import WorkoutCreate, WorkoutResponse
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/{username}/commit", response_model=WorkoutResponse)
def post_workout(username: str, workout: WorkoutCreate, db: Session = Depends(get_db)):
    # username으로 User 조회
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 운동 기록 생성
    db_workout = Workout(
        user_id=user.id,
        exercise_type=workout.exercise_type,
        duration=workout.duration,
        sets=workout.sets,
        reps_per_set=workout.reps_per_set,
        intensity=workout.intensity,
        commit_message=workout.commit_message,
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    
    return db_workout

@router.get("/{username}/workout", response_model=List[WorkoutResponse])
def get_workout(username: str, db: Session = Depends(get_db)):
    # username으로 User 조회
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    workouts = db.query(Workout).filter(Workout.user_id == user.id).all()
    return workouts 

@router.patch("/{username}/workout/{workout_id}", response_model=WorkoutCreate)
def update_workout(username: str, workout_id: int, workout: WorkoutCreate, db: Session = Depends(get_db)):
    # username으로 사용자 조회
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")

    # 운동 기록 조회 (user_id도 확인)
    existing_workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == user.id).first()
    
    # 운동 기록이 존재하지 않으면 404 에러 반환
    if not existing_workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    # 운동 기록 수정
    if workout.exercise_type:
        existing_workout.exercise_type = workout.exercise_type
    if workout.duration:
        existing_workout.duration = workout.duration
    if workout.sets:
        existing_workout.sets = workout.sets
    if workout.reps_per_set:
        existing_workout.reps_per_set = workout.reps_per_set
    if workout.intensity:
        existing_workout.intensity = workout.intensity
    if workout.commit_message:
        existing_workout.commit_message = workout.commit_message
    
    db.commit()
    db.refresh(existing_workout)
    
    return JSONResponse(status_code=200, content={"message": "Workout updated successfully"})


@router.delete("/{username}/workout/{workout_id}", status_code=204)
def delete_workout(username: str, workout_id: int, db: Session = Depends(get_db)):
    # 사용자 확인
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 운동 기록 확인
    workout = db.query(Workout).filter(
        Workout.id == workout_id, 
        Workout.user_id == user.id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    # 운동 기록 삭제
    db.delete(workout)
    db.commit()
    return {"message": "Workout deleted successfully"}