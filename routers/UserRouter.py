from fastapi import APIRouter, Depends
from controller.Usercontroller import UserController
from sqlalchemy.orm import Session
from database.db import get_db
from models.User import User
from models.UserISchema import UserCreate

router = APIRouter()


@router.get("/users/create", tags=["Users"], response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserController(db_session=db).create_user(user)
