from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import AlarmIntelligenceResult
from app.repositories.base import BaseRepository


class AlarmIntelligenceRepository(BaseRepository[AlarmIntelligenceResult]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, AlarmIntelligenceResult)

    def list_recent(self, limit: int = 50) -> list[AlarmIntelligenceResult]:
        statement = (
            select(AlarmIntelligenceResult)
            .order_by(AlarmIntelligenceResult.created_at.desc())
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def get_result(self, id: UUID) -> AlarmIntelligenceResult | None:
        return self.db.get(AlarmIntelligenceResult, id)
