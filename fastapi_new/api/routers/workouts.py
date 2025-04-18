from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter,Depends,HTTPException,status
from api.models import workout
from api.deps import db_dependency,user_dependency

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    pass

@router.get("/")
def get_workout(db:db_dependency,user: user_dependency,workout_id:int):
    return db.query(workout).filter(workout.id == workout_id).first()

@router.get("/workouts")
def get_workouts(db:db_dependency,user: user_dependency):
    return db.query(workout).all()

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_workout(db:db_dependency,user: user_dependency,workout_create:WorkoutCreate):
    db_workout = workout(**workout_create.model_dump(),user_id=user.get("id"))
    db.add(db_workout)
    db.commit()
    db.refresh
    return db_workout

@router.delete("/")
def delete_workout(db:db_dependency,user: user_dependency,workout_id:int):
    db_workout = db.query(workout).filter(workout.id == workout_id).first()
    if db_workout:
        db.delete(db.workout)
        db.commit()
    return db_workout