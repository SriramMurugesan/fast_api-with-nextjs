from pydantic import BaseModel
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import joinedload
from api.models import Routine as RoutineModel, Workout
from api.deps import db_dependency, user_dependency

router = APIRouter(
    prefix="/routines",
    tags=["Routines"]
)

class RoutineBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoutineCreate(RoutineBase):
    workouts: List[int] = []

@router.get("/")
def get_routines(db: db_dependency, user: user_dependency):
    return db.query(RoutineModel).options(joinedload(RoutineModel.workouts)).filter(RoutineModel.user_id == user.get('user_id')).all()

@router.post("/")
def create_routine(db: db_dependency, user: user_dependency, routine: RoutineCreate):
    db_routine = RoutineModel(name=routine.name, description=routine.description, user_id=user.get('user_id'))
    for workout_id in routine.workouts:
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            db_routine.workouts.append(workout)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    db_routines = db.query(RoutineModel).options(joinedload(RoutineModel.workouts)).filter(RoutineModel.id == db_routine.id).first()
    return db_routines

@router.delete("/")
def delete_routine(db: db_dependency, user: user_dependency, routine_id: int):
    db_routine = db.query(RoutineModel).filter(RoutineModel.id == routine_id).first()
    if db_routine:
        db.delete(db_routine)
        db.commit()
    return db_routine
