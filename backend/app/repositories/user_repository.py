from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, User)

    def get(self, id: UUID) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.role))
            .where(User.id == id)
        )
        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.role))
            .where(User.email == email)
        )
        return self.db.scalar(statement)

    def get_by_username(self, username: str) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.role))
            .where(User.username == username)
        )
        return self.db.scalar(statement)

    def get_by_login(self, login: str) -> User | None:
        statement = (
            select(User)
            .options(selectinload(User.role))
            .where(or_(User.email == login, User.username == login))
        )
        return self.db.scalar(statement)

