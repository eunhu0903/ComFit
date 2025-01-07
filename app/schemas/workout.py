from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from db.models import IntensityEnum

class WorkoutCreate(BaseModel):
    exercise_type: str 
    duration: float  
    sets: int 
    reps_per_set: int 
    intensity: IntensityEnum
    commit_message: Optional[str] = None

class WorkoutResponse(BaseModel):
    id: int
    exercise_type: str
    duration: float
    sets: int
    reps_per_set: int
    intensity: IntensityEnum
    commit_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True