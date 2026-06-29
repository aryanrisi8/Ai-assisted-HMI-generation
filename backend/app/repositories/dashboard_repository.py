from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from app.models import Dashboard
from app.repositories.base import BaseRepository


class DashboardRepository(BaseRepository[Dashboard]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Dashboard)

    def get_with_layouts(self, id: UUID) -> Dashboard | None:
        statement = (
            select(Dashboard)
            .options(selectinload(Dashboard.layouts))
            .where(Dashboard.id == id)
        )
        return self.db.scalar(statement)

    def get_by_slug(self, slug: str) -> Dashboard | None:
        statement = select(Dashboard).where(Dashboard.slug == slug)
        return self.db.scalar(statement)

    def list_by_owner(self, owner_id: UUID, offset: int = 0, limit: int = 100) -> list[Dashboard]:
        statement = (
            select(Dashboard)
            .where(Dashboard.owner_id == owner_id)
            .order_by(Dashboard.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def count_by_owner(self, owner_id: UUID) -> int:
        statement = select(func.count()).select_from(Dashboard).where(
            Dashboard.owner_id == owner_id
        )
        return self.db.scalar(statement) or 0
