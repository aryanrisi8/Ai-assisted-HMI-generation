from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class UUIDPrimaryKeyMixin:
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"


class SystemStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    DECOMMISSIONED = "decommissioned"


class SensorStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAULTED = "faulted"
    CALIBRATION = "calibration"


class SignalDataType(str, Enum):
    BOOLEAN = "boolean"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    ENUM = "enum"


class SignalDirection(str, Enum):
    INPUT = "input"
    OUTPUT = "output"
    BIDIRECTIONAL = "bidirectional"
    INTERNAL = "internal"


class AlarmSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlarmState(str, Enum):
    NORMAL = "normal"
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    SHELVED = "shelved"
    CLEARED = "cleared"


class AlarmHistoryEventType(str, Enum):
    RAISED = "raised"
    ACKNOWLEDGED = "acknowledged"
    SHELVED = "shelved"
    UNSHELVED = "unshelved"
    CLEARED = "cleared"
    COMMENTED = "commented"
    PRIORITY_CHANGED = "priority_changed"
    CORRELATED = "correlated"


class DashboardStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ComponentKind(str, Enum):
    DISPLAY = "display"
    CONTROL = "control"
    CHART = "chart"
    ALARM = "alarm"
    CONTAINER = "container"
    SYMBOL = "symbol"


class AssistantLogType(str, Enum):
    HMI_GENERATION = "hmi_generation"
    ALARM_INTELLIGENCE = "alarm_intelligence"
    SCHEMA_VALIDATION = "schema_validation"
    USER_QUERY = "user_query"


class Role(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    permissions: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    is_system_role: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    users: Mapped[list["User"]] = relationship(
        back_populates="role", cascade="save-update"
    )

    __table_args__ = (
        Index("ix_roles_name", "name"),
        CheckConstraint("length(name) >= 2", name="ck_roles_name_min_length"),
    )


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    role_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[UserStatus] = mapped_column(
        SQLEnum(UserStatus, name="user_status"), nullable=False, default=UserStatus.ACTIVE
    )
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    role: Mapped["Role"] = relationship(back_populates="users")
    dashboards: Mapped[list["Dashboard"]] = relationship(back_populates="owner")
    assistant_logs: Mapped[list["AssistantLog"]] = relationship(back_populates="user")
    alarm_history_events: Mapped[list["AlarmHistory"]] = relationship(
        back_populates="actor"
    )

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_username", "username"),
        Index("ix_users_role_id", "role_id"),
        CheckConstraint("position('@' in email) > 1", name="ck_users_email_format"),
        CheckConstraint("length(username) >= 3", name="ck_users_username_min_length"),
    )


class IndustrialSystem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "industrial_systems"

    parent_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("industrial_systems.id", ondelete="SET NULL")
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    code: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    system_type: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[SystemStatus] = mapped_column(
        SQLEnum(SystemStatus, name="system_status"),
        nullable=False,
        default=SystemStatus.ACTIVE,
    )
    location: Mapped[str | None] = mapped_column(String(160))
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    parent: Mapped["IndustrialSystem | None"] = relationship(
        remote_side="IndustrialSystem.id", back_populates="children"
    )
    children: Mapped[list["IndustrialSystem"]] = relationship(back_populates="parent")
    signals: Mapped[list["Signal"]] = relationship(
        back_populates="industrial_system", cascade="all, delete-orphan"
    )
    sensors: Mapped[list["Sensor"]] = relationship(
        back_populates="industrial_system", cascade="all, delete-orphan"
    )
    dashboards: Mapped[list["Dashboard"]] = relationship(back_populates="industrial_system")

    __table_args__ = (
        Index("ix_industrial_systems_parent_id", "parent_id"),
        Index("ix_industrial_systems_code", "code"),
        Index("ix_industrial_systems_type_status", "system_type", "status"),
        CheckConstraint("length(code) >= 2", name="ck_industrial_systems_code_min_length"),
    )


class Sensor(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "sensors"

    industrial_system_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("industrial_systems.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    sensor_type: Mapped[str] = mapped_column(String(80), nullable=False)
    manufacturer: Mapped[str | None] = mapped_column(String(120))
    model: Mapped[str | None] = mapped_column(String(120))
    serial_number: Mapped[str | None] = mapped_column(String(120))
    location: Mapped[str | None] = mapped_column(String(160))
    status: Mapped[SensorStatus] = mapped_column(
        SQLEnum(SensorStatus, name="sensor_status"),
        nullable=False,
        default=SensorStatus.ACTIVE,
    )
    calibration_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    industrial_system: Mapped["IndustrialSystem"] = relationship(back_populates="sensors")
    signals: Mapped[list["Signal"]] = relationship(back_populates="sensor")

    __table_args__ = (
        Index("ix_sensors_industrial_system_id", "industrial_system_id"),
        Index("ix_sensors_code", "code"),
        Index("ix_sensors_type_status", "sensor_type", "status"),
        UniqueConstraint("industrial_system_id", "name", name="uq_sensors_system_name"),
        CheckConstraint("length(code) >= 2", name="ck_sensors_code_min_length"),
    )


class Signal(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "signals"

    industrial_system_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("industrial_systems.id", ondelete="CASCADE"),
        nullable=False,
    )
    sensor_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("sensors.id", ondelete="SET NULL")
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    tag: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    data_type: Mapped[SignalDataType] = mapped_column(
        SQLEnum(SignalDataType, name="signal_data_type"), nullable=False
    )
    direction: Mapped[SignalDirection] = mapped_column(
        SQLEnum(SignalDirection, name="signal_direction"), nullable=False
    )
    engineering_unit: Mapped[str | None] = mapped_column(String(40))
    min_value: Mapped[float | None] = mapped_column(Float)
    max_value: Mapped[float | None] = mapped_column(Float)
    current_value: Mapped[dict | None] = mapped_column(JSON)
    quality: Mapped[str | None] = mapped_column(String(40))
    source_address: Mapped[str | None] = mapped_column(String(255))
    scan_rate_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=1000)
    is_writable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    industrial_system: Mapped["IndustrialSystem"] = relationship(back_populates="signals")
    sensor: Mapped["Sensor | None"] = relationship(back_populates="signals")
    alarms: Mapped[list["Alarm"]] = relationship(back_populates="signal")

    __table_args__ = (
        Index("ix_signals_industrial_system_id", "industrial_system_id"),
        Index("ix_signals_sensor_id", "sensor_id"),
        Index("ix_signals_tag", "tag"),
        Index("ix_signals_data_type", "data_type"),
        UniqueConstraint("industrial_system_id", "name", name="uq_signals_system_name"),
        CheckConstraint("scan_rate_ms > 0", name="ck_signals_scan_rate_positive"),
        CheckConstraint(
            "(min_value IS NULL OR max_value IS NULL OR min_value <= max_value)",
            name="ck_signals_min_lte_max",
        ),
    )


class Alarm(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "alarms"

    signal_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("signals.id", ondelete="CASCADE"), nullable=False
    )
    code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    severity: Mapped[AlarmSeverity] = mapped_column(
        SQLEnum(AlarmSeverity, name="alarm_severity"), nullable=False
    )
    state: Mapped[AlarmState] = mapped_column(
        SQLEnum(AlarmState, name="alarm_state"), nullable=False, default=AlarmState.NORMAL
    )
    condition_expression: Mapped[str] = mapped_column(Text, nullable=False)
    setpoint: Mapped[float | None] = mapped_column(Float)
    deadband: Mapped[float | None] = mapped_column(Float)
    delay_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    requires_ack: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cleared_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    signal: Mapped["Signal"] = relationship(back_populates="alarms")
    history: Mapped[list["AlarmHistory"]] = relationship(
        back_populates="alarm", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_alarms_signal_id", "signal_id"),
        Index("ix_alarms_code", "code"),
        Index("ix_alarms_state_severity", "state", "severity"),
        Index("ix_alarms_active_at", "active_at"),
        UniqueConstraint("signal_id", "name", name="uq_alarms_signal_name"),
        CheckConstraint("delay_ms >= 0", name="ck_alarms_delay_non_negative"),
        CheckConstraint(
            "deadband IS NULL OR deadband >= 0", name="ck_alarms_deadband_non_negative"
        ),
    )


class AlarmHistory(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "alarm_history"

    alarm_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("alarms.id", ondelete="CASCADE"), nullable=False
    )
    actor_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    event_type: Mapped[AlarmHistoryEventType] = mapped_column(
        SQLEnum(AlarmHistoryEventType, name="alarm_history_event_type"), nullable=False
    )
    previous_state: Mapped[AlarmState | None] = mapped_column(
        SQLEnum(AlarmState, name="alarm_state")
    )
    new_state: Mapped[AlarmState | None] = mapped_column(
        SQLEnum(AlarmState, name="alarm_state")
    )
    value_snapshot: Mapped[dict | None] = mapped_column(JSON)
    message: Mapped[str | None] = mapped_column(Text)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    alarm: Mapped["Alarm"] = relationship(back_populates="history")
    actor: Mapped["User | None"] = relationship(back_populates="alarm_history_events")

    __table_args__ = (
        Index("ix_alarm_history_alarm_id_occurred_at", "alarm_id", "occurred_at"),
        Index("ix_alarm_history_actor_id", "actor_id"),
        Index("ix_alarm_history_event_type", "event_type"),
        Index("ix_alarm_history_occurred_at", "occurred_at"),
    )


class TemplateCategory(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "template_categories"

    parent_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("template_categories.id", ondelete="SET NULL")
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    parent: Mapped["TemplateCategory | None"] = relationship(
        remote_side="TemplateCategory.id", back_populates="children"
    )
    children: Mapped[list["TemplateCategory"]] = relationship(back_populates="parent")
    templates: Mapped[list["Template"]] = relationship(back_populates="category")

    __table_args__ = (
        Index("ix_template_categories_parent_id", "parent_id"),
        Index("ix_template_categories_slug", "slug"),
        UniqueConstraint("parent_id", "name", name="uq_template_categories_parent_name"),
    )


class Template(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "templates"

    category_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("template_categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    industry: Mapped[str] = mapped_column(String(120), nullable=False, default="general")
    description: Mapped[str | None] = mapped_column(Text)
    layout_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    components_json: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    schema_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    preview_image_url: Mapped[str | None] = mapped_column(String(500))
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    category: Mapped["TemplateCategory"] = relationship(back_populates="templates")
    dashboards: Mapped[list["Dashboard"]] = relationship(back_populates="template")

    __table_args__ = (
        Index("ix_templates_category_id", "category_id"),
        Index("ix_templates_slug", "slug"),
        Index("ix_templates_industry", "industry"),
        Index("ix_templates_active", "is_active"),
        CheckConstraint("version > 0", name="ck_templates_version_positive"),
        CheckConstraint("length(industry) >= 1", name="ck_templates_industry_min_length"),
    )


class Dashboard(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "dashboards"

    owner_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    industrial_system_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("industrial_systems.id", ondelete="SET NULL")
    )
    template_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("templates.id", ondelete="SET NULL")
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(160), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[DashboardStatus] = mapped_column(
        SQLEnum(DashboardStatus, name="dashboard_status"),
        nullable=False,
        default=DashboardStatus.DRAFT,
    )
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    owner: Mapped["User"] = relationship(back_populates="dashboards")
    industrial_system: Mapped["IndustrialSystem | None"] = relationship(
        back_populates="dashboards"
    )
    template: Mapped["Template | None"] = relationship(back_populates="dashboards")
    layouts: Mapped[list["DashboardLayout"]] = relationship(
        back_populates="dashboard", cascade="all, delete-orphan"
    )
    components: Mapped[list["Component"]] = relationship(
        back_populates="dashboard", cascade="all, delete-orphan"
    )
    assistant_logs: Mapped[list["AssistantLog"]] = relationship(back_populates="dashboard")

    __table_args__ = (
        Index("ix_dashboards_owner_id", "owner_id"),
        Index("ix_dashboards_industrial_system_id", "industrial_system_id"),
        Index("ix_dashboards_template_id", "template_id"),
        Index("ix_dashboards_status", "status"),
        Index("ix_dashboards_slug", "slug"),
        CheckConstraint("schema_version > 0", name="ck_dashboards_schema_version_positive"),
    )


class DashboardLayout(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "dashboard_layouts"

    dashboard_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("dashboards.id", ondelete="CASCADE"), nullable=False
    )
    breakpoint: Mapped[str] = mapped_column(String(40), nullable=False)
    columns: Mapped[int] = mapped_column(Integer, nullable=False)
    row_height: Mapped[int] = mapped_column(Integer, nullable=False)
    layout_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    dashboard: Mapped["Dashboard"] = relationship(back_populates="layouts")

    __table_args__ = (
        Index("ix_dashboard_layouts_dashboard_id", "dashboard_id"),
        UniqueConstraint("dashboard_id", "breakpoint", name="uq_dashboard_layout_breakpoint"),
        CheckConstraint("columns > 0", name="ck_dashboard_layouts_columns_positive"),
        CheckConstraint("row_height > 0", name="ck_dashboard_layouts_row_height_positive"),
    )


class Component(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "components"

    dashboard_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("dashboards.id", ondelete="CASCADE"), nullable=False
    )
    signal_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("signals.id", ondelete="SET NULL")
    )
    parent_component_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("components.id", ondelete="CASCADE")
    )
    component_key: Mapped[str] = mapped_column(String(120), nullable=False)
    type: Mapped[str] = mapped_column(String(120), nullable=False)
    kind: Mapped[ComponentKind] = mapped_column(
        SQLEnum(ComponentKind, name="component_kind"), nullable=False
    )
    title: Mapped[str | None] = mapped_column(String(160))
    props_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    style_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    binding_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    interaction_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    visibility_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    registry_version: Mapped[str] = mapped_column(String(40), nullable=False, default="1.0.0")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    dashboard: Mapped["Dashboard"] = relationship(back_populates="components")
    signal: Mapped["Signal | None"] = relationship()
    parent_component: Mapped["Component | None"] = relationship(
        remote_side="Component.id", back_populates="child_components"
    )
    child_components: Mapped[list["Component"]] = relationship(
        back_populates="parent_component", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_components_dashboard_id", "dashboard_id"),
        Index("ix_components_signal_id", "signal_id"),
        Index("ix_components_parent_component_id", "parent_component_id"),
        Index("ix_components_type", "type"),
        UniqueConstraint("dashboard_id", "component_key", name="uq_components_dashboard_key"),
        CheckConstraint("length(component_key) >= 2", name="ck_components_key_min_length"),
    )


class AssistantLog(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "assistant_logs"

    user_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL")
    )
    dashboard_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("dashboards.id", ondelete="SET NULL")
    )
    log_type: Mapped[AssistantLogType] = mapped_column(
        SQLEnum(AssistantLogType, name="assistant_log_type"), nullable=False
    )
    prompt: Mapped[str | None] = mapped_column(Text)
    response: Mapped[str | None] = mapped_column(Text)
    request_json: Mapped[dict | None] = mapped_column(JSON)
    response_json: Mapped[dict | None] = mapped_column(JSON)
    model_name: Mapped[str | None] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="completed")
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User | None"] = relationship(back_populates="assistant_logs")
    dashboard: Mapped["Dashboard | None"] = relationship(back_populates="assistant_logs")

    __table_args__ = (
        Index("ix_assistant_logs_user_id", "user_id"),
        Index("ix_assistant_logs_dashboard_id", "dashboard_id"),
        Index("ix_assistant_logs_log_type", "log_type"),
        Index("ix_assistant_logs_created_at", "created_at"),
        CheckConstraint(
            "latency_ms IS NULL OR latency_ms >= 0",
            name="ck_assistant_logs_latency_non_negative",
        ),
    )


class AlarmIntelligenceResult(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "alarm_intelligence_results"

    root_cause: Mapped[str] = mapped_column(String(255), nullable=False)
    confidence: Mapped[int] = mapped_column(Integer, nullable=False)
    affected_signals: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    severity_ranking: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    suppressed_duplicates: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    grouped_incidents: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    incident_clusters: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    input_event_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_alarm_intelligence_results_created_at", "created_at"),
        Index("ix_alarm_intelligence_results_root_cause", "root_cause"),
        CheckConstraint(
            "confidence >= 0 AND confidence <= 100",
            name="ck_alarm_intelligence_results_confidence_range",
        ),
        CheckConstraint(
            "suppressed_duplicates >= 0",
            name="ck_alarm_intelligence_results_suppressed_non_negative",
        ),
        CheckConstraint(
            "input_event_count >= 0",
            name="ck_alarm_intelligence_results_input_count_non_negative",
        ),
    )
