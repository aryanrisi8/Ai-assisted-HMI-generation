from uuid import UUID

from fastapi import status
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.models import Alarm, IndustrialSystem, Sensor, Signal
from app.repositories.metadata_repository import MetadataRepository
from app.schemas import (
    AlarmRead,
    MetadataCreate,
    MetadataRead,
    MetadataSignalCreate,
    MetadataUpdate,
    SensorRead,
    SignalRead,
)


class MetadataService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.metadata = MetadataRepository(db)

    def create(self, payload: MetadataCreate) -> MetadataRead:
        self._ensure_unique_create_payload(payload)

        industrial_system = IndustrialSystem(**payload.industrial_system.model_dump())
        self.db.add(industrial_system)
        self.db.flush()

        sensor_map = self._create_sensors(industrial_system, payload.sensors)
        self._create_signals_and_alarms(industrial_system, sensor_map, payload.signals)

        self.db.commit()
        created = self.metadata.get_metadata(industrial_system.id)
        if created is None:
            raise AppException("Created metadata could not be loaded.")
        return self._to_read(created)

    def list(self, offset: int = 0, limit: int = 100) -> list[MetadataRead]:
        records = self.metadata.list_metadata(offset=offset, limit=limit)
        return [self._to_read(record) for record in records]

    def get(self, id: UUID) -> MetadataRead:
        record = self._get_record(id)
        return self._to_read(record)

    def update(self, id: UUID, payload: MetadataUpdate) -> MetadataRead:
        record = self._get_record(id)
        self._ensure_update_does_not_conflict(record, payload)

        if payload.industrial_system:
            for field, value in payload.industrial_system.model_dump(
                exclude_unset=True
            ).items():
                setattr(record, field, value)

        if payload.sensors is not None or payload.signals is not None:
            self._replace_nested_metadata(record, payload)

        self.db.commit()
        updated = self.metadata.get_metadata(id)
        if updated is None:
            raise AppException("Updated metadata could not be loaded.")
        return self._to_read(updated)

    def delete(self, id: UUID) -> None:
        record = self._get_record(id)
        self.metadata.delete(record)
        self.db.commit()

    def _get_record(self, id: UUID) -> IndustrialSystem:
        record = self.metadata.get_metadata(id)
        if record is None:
            raise AppException(
                message="Metadata record not found.",
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="metadata_not_found",
            )
        return record

    def _ensure_unique_create_payload(self, payload: MetadataCreate) -> None:
        if self.metadata.get_by_code(payload.industrial_system.code):
            raise AppException(
                message="Industrial system code already exists.",
                status_code=status.HTTP_409_CONFLICT,
                error_code="industrial_system_code_exists",
            )

        for sensor in payload.sensors:
            if self.metadata.get_sensor_by_code(sensor.code):
                raise AppException(
                    message=f"Sensor code already exists: {sensor.code}.",
                    status_code=status.HTTP_409_CONFLICT,
                    error_code="sensor_code_exists",
                )

        for signal in payload.signals:
            if self.metadata.get_signal_by_tag(signal.tag):
                raise AppException(
                    message=f"Signal tag already exists: {signal.tag}.",
                    status_code=status.HTTP_409_CONFLICT,
                    error_code="signal_tag_exists",
                )
            for alarm in signal.alarm_thresholds:
                if self.metadata.get_alarm_by_code(alarm.code):
                    raise AppException(
                        message=f"Alarm code already exists: {alarm.code}.",
                        status_code=status.HTTP_409_CONFLICT,
                        error_code="alarm_code_exists",
                    )

    def _ensure_update_does_not_conflict(
        self,
        record: IndustrialSystem,
        payload: MetadataUpdate,
    ) -> None:
        if payload.industrial_system and payload.industrial_system.code:
            existing = self.metadata.get_by_code(payload.industrial_system.code)
            if existing and existing.id != record.id:
                raise AppException(
                    message="Industrial system code already exists.",
                    status_code=status.HTTP_409_CONFLICT,
                    error_code="industrial_system_code_exists",
                )

        current_sensor_ids = {sensor.id for sensor in record.sensors}
        for sensor in payload.sensors or []:
            existing = self.metadata.get_sensor_by_code(sensor.code)
            if existing and existing.id not in current_sensor_ids:
                raise AppException(
                    message=f"Sensor code already exists: {sensor.code}.",
                    status_code=status.HTTP_409_CONFLICT,
                    error_code="sensor_code_exists",
                )

        current_signal_ids = {signal.id for signal in record.signals}
        current_alarm_ids = {
            alarm.id for signal in record.signals for alarm in signal.alarms
        }
        for signal in payload.signals or []:
            existing_signal = self.metadata.get_signal_by_tag(signal.tag)
            if existing_signal and existing_signal.id not in current_signal_ids:
                raise AppException(
                    message=f"Signal tag already exists: {signal.tag}.",
                    status_code=status.HTTP_409_CONFLICT,
                    error_code="signal_tag_exists",
                )
            for alarm in signal.alarm_thresholds:
                existing_alarm = self.metadata.get_alarm_by_code(alarm.code)
                if existing_alarm and existing_alarm.id not in current_alarm_ids:
                    raise AppException(
                        message=f"Alarm code already exists: {alarm.code}.",
                        status_code=status.HTTP_409_CONFLICT,
                        error_code="alarm_code_exists",
                    )

    def _create_sensors(
        self,
        industrial_system: IndustrialSystem,
        sensors: list,
    ) -> dict[str, Sensor]:
        sensor_map: dict[str, Sensor] = {}
        for sensor_payload in sensors:
            sensor = Sensor(
                industrial_system_id=industrial_system.id,
                **sensor_payload.model_dump(),
            )
            self.db.add(sensor)
            self.db.flush()
            sensor_map[sensor.code] = sensor
        return sensor_map

    def _create_signals_and_alarms(
        self,
        industrial_system: IndustrialSystem,
        sensor_map: dict[str, Sensor],
        signals: list[MetadataSignalCreate],
    ) -> None:
        for signal_payload in signals:
            sensor_id = None
            if signal_payload.sensor_code:
                sensor = sensor_map.get(signal_payload.sensor_code)
                if sensor is None:
                    raise AppException(
                        message=f"Unknown sensor code: {signal_payload.sensor_code}.",
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        error_code="unknown_sensor_code",
                    )
                sensor_id = sensor.id

            signal_data = signal_payload.model_dump(
                exclude={"sensor_code", "alarm_thresholds"}
            )
            signal = Signal(
                industrial_system_id=industrial_system.id,
                sensor_id=sensor_id,
                **signal_data,
            )
            self.db.add(signal)
            self.db.flush()

            for alarm_payload in signal_payload.alarm_thresholds:
                alarm_metadata = dict(alarm_payload.metadata_json)
                alarm_metadata["criticality_level"] = alarm_payload.criticality_level
                alarm = Alarm(
                    signal_id=signal.id,
                    **alarm_payload.model_dump(
                        exclude={"criticality_level", "metadata_json"}
                    ),
                    metadata_json=alarm_metadata,
                )
                self.db.add(alarm)

    def _replace_nested_metadata(
        self,
        record: IndustrialSystem,
        payload: MetadataUpdate,
    ) -> None:
        if payload.signals is not None:
            record.signals.clear()
            self.db.flush()

        if payload.sensors is not None:
            record.sensors.clear()
            self.db.flush()

        sensor_map = {sensor.code: sensor for sensor in record.sensors}
        if payload.sensors is not None:
            sensor_map = self._create_sensors(record, payload.sensors)

        if payload.signals is not None:
            self._create_signals_and_alarms(record, sensor_map, payload.signals)

    def _to_read(self, record: IndustrialSystem) -> MetadataRead:
        alarms = [alarm for signal in record.signals for alarm in signal.alarms]
        return MetadataRead(
            industrial_system=record,
            sensors=[SensorRead.model_validate(sensor) for sensor in record.sensors],
            signals=[SignalRead.model_validate(signal) for signal in record.signals],
            alarms=[AlarmRead.model_validate(alarm) for alarm in alarms],
        )
