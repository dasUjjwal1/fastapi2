from typing import List
from fastapi import HTTPException
from sqlalchemy import Exists
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.Pagination import PaginationCreate
from models.User import User
from models.UserISchema import UserCreate


class UserController:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: int) -> User:
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, user_email: str) -> User:
        return self.db_session.query(User).filter(User.email == user_email).first()

    def get_user(self, pagination: PaginationCreate) -> List[User]:
        return (
            self.db_session.query(User)
            .offset(pagination.skip)
            .limit(pagination.limit)
            .all()
        )

    async def create_user(self, payload: UserCreate) -> User:
        is_user: Exists = (
            self.db_session.query(User).filter(User.email == payload.email).exists()
        )

        if is_user._execute_on_scalar:
            raise HTTPException(status_code=404, detail="User already registered")
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(payload.password)
        user = User(email=payload.email, password=hashed_password)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
