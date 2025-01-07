from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Workout, User
from schemas.workout import WorkoutCreate, WorkoutResponse
from typing import List

router = APIRouter()

@router.post("/{user_id}/commit_workout", response_model=WorkoutResponse)
def post_workout(user_id: int, workout: WorkoutCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    
    db_workout = Workout(
        user_id=user_id,
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

@router.get("/{user_id}/workout", response_model=List[WorkoutResponse])
def get_workout(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    
    workouts = db.query(Workout).filter(Workout.user_id == user_id).all()
    return workouts 