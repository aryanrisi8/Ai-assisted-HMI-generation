from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session


ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, db: Session, model: type[ModelType]) -> None:
        self.db = db
        self.model = model

    def get(self, id: UUID) -> ModelType | None:
        return self.db.get(self.model, id)

    def list(self, offset: int = 0, limit: int = 100) -> list[ModelType]:
        statement = select(self.model).offset(offset).limit(limit)
        return list(self.db.scalars(statement).all())

    def add(self, instance: ModelType) -> ModelType:
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance

    def delete(self, instance: ModelType) -> None:
        self.db.delete(instance)
        self.db.flush()

