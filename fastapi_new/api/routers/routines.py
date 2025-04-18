from pydantic import BaseModel
from typing import Optional, List
from fastapi import APIRouter,Depends,HTTPException,status
from api.models import Routine,Workout
from api.deps import db_dependency,user_dependency

router = APIRouter(
    prefix="/routines",
    tags=["Routines"]
)

class Routine(BaseModel):
    name: str
    description: Optional[str] = None

class RoutineCreate(Routine):
    workouts: List[int]= []

@router.get("/")
def get_routines(db:db_dependency,user:user_dependency):
    return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user.id==user.get('id')).all()

@