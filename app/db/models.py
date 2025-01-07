import enum
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class IntensityEnum(enum.Enum):
    LIGHT = "가벼운"
    MODERATE = "보통"
    HEAVY = "강력한"

class User(Base):
    __tablename__='users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(10), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    workouts = relationship("Workout", back_populates="user")

class Workout(Base):
    __tablename__='workouts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    exercise_type = Column(String(100), index=True)
    duration = Column(Float)
    sets = Column(Integer)
    reps_per_set = Column(Integer)
    intensity = Column(Enum(IntensityEnum), nullable=False)
    commit_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workouts")
