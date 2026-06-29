from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Alarm, IndustrialSystem, Sensor, Signal
from app.repositories.base import BaseRepository


class MetadataRepository(BaseRepository[IndustrialSystem]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, IndustrialSystem)

    def list_metadata(self, offset: int = 0, limit: int = 100) -> list[IndustrialSystem]:
        statement = (
            select(IndustrialSystem)
            .options(
                selectinload(IndustrialSystem.sensors),
                selectinload(IndustrialSystem.signals).selectinload(Signal.alarms),
            )
            .order_by(IndustrialSystem.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(statement).all())

    def get_metadata(self, id: UUID) -> IndustrialSystem | None:
        statement = (
            select(IndustrialSystem)
            .options(
                selectinload(IndustrialSystem.sensors),
                selectinload(IndustrialSystem.signals).selectinload(Signal.alarms),
            )
            .where(IndustrialSystem.id == id)
        )
        return self.db.scalar(statement)

    def get_by_code(self, code: str) -> IndustrialSystem | None:
        statement = select(IndustrialSystem).where(IndustrialSystem.code == code)
        return self.db.scalar(statement)

    def get_sensor_by_code(self, code: str) -> Sensor | None:
        statement = select(Sensor).where(Sensor.code == code)
        return self.db.scalar(statement)

    def get_signal_by_tag(self, tag: str) -> Signal | None:
        statement = select(Signal).where(Signal.tag == tag)
        return self.db.scalar(statement)

    def get_alarm_by_code(self, code: str) -> Alarm | None:
        statement = select(Alarm).where(Alarm.code == code)
        return self.db.scalar(statement)

