from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.models import (
    AlarmHistoryEventType,
    AlarmSeverity,
    AlarmState,
    AssistantLogType,
    ComponentKind,
    DashboardStatus,
    SensorStatus,
    SignalDataType,
    SignalDirection,
    SystemStatus,
    UserStatus,
)


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str | None = None
    permissions: dict[str, Any] = Field(default_factory=dict)
    is_system_role: bool = False


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = None
    permissions: dict[str, Any] | None = None
    is_system_role: bool | None = None


class RoleRead(RoleBase, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserBase(BaseModel):
    role_id: UUID
    email: EmailStr
    username: str = Field(min_length=3, max_length=80)
    full_name: str = Field(min_length=1, max_length=160)
    status: UserStatus = UserStatus.ACTIVE
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str = Field(min_length=12, max_length=128)


class UserUpdate(BaseModel):
    role_id: UUID | None = None
    email: EmailStr | None = None
    username: str | None = Field(default=None, min_length=3, max_length=80)
    full_name: str | None = Field(default=None, min_length=1, max_length=160)
    status: UserStatus | None = None
    is_superuser: bool | None = None
    password: str | None = Field(default=None, min_length=12, max_length=128)


class UserRead(UserBase, ORMModel):
    id: UUID
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime
    role: RoleRead | None = None


class IndustrialSystemBase(BaseModel):
    parent_id: UUID | None = None
    name: str = Field(min_length=1, max_length=160)
    code: str = Field(min_length=2, max_length=80)
    description: str | None = None
    system_type: str = Field(min_length=1, max_length=80)
    status: SystemStatus = SystemStatus.ACTIVE
    location: str | None = Field(default=None, max_length=160)
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class IndustrialSystemCreate(IndustrialSystemBase):
    pass


class IndustrialSystemUpdate(BaseModel):
    parent_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=160)
    code: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = None
    system_type: str | None = Field(default=None, min_length=1, max_length=80)
    status: SystemStatus | None = None
    location: str | None = Field(default=None, max_length=160)
    metadata_json: dict[str, Any] | None = None


class IndustrialSystemRead(IndustrialSystemBase, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class SensorBase(BaseModel):
    industrial_system_id: UUID
    name: str = Field(min_length=1, max_length=160)
    code: str = Field(min_length=2, max_length=120)
    sensor_type: str = Field(min_length=1, max_length=80)
    manufacturer: str | None = Field(default=None, max_length=120)
    model: str | None = Field(default=None, max_length=120)
    serial_number: str | None = Field(default=None, max_length=120)
    location: str | None = Field(default=None, max_length=160)
    status: SensorStatus = SensorStatus.ACTIVE
    calibration_due_at: datetime | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    industrial_system_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=160)
    code: str | None = Field(default=None, min_length=2, max_length=120)
    sensor_type: str | None = Field(default=None, min_length=1, max_length=80)
    manufacturer: str | None = Field(default=None, max_length=120)
    model: str | None = Field(default=None, max_length=120)
    serial_number: str | None = Field(default=None, max_length=120)
    location: str | None = Field(default=None, max_length=160)
    status: SensorStatus | None = None
    calibration_due_at: datetime | None = None
    metadata_json: dict[str, Any] | None = None


class SensorRead(SensorBase, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class SignalBase(BaseModel):
    industrial_system_id: UUID
    sensor_id: UUID | None = None
    name: str = Field(min_length=1, max_length=160)
    tag: str = Field(min_length=1, max_length=160)
    description: str | None = None
    data_type: SignalDataType
    direction: SignalDirection
    engineering_unit: str | None = Field(default=None, max_length=40)
    min_value: float | None = None
    max_value: float | None = None
    current_value: dict[str, Any] | None = None
    quality: str | None = Field(default=None, max_length=40)
    source_address: str | None = Field(default=None, max_length=255)
    scan_rate_ms: int = Field(default=1000, gt=0)
    is_writable: bool = False
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class SignalCreate(SignalBase):
    pass


class SignalUpdate(BaseModel):
    industrial_system_id: UUID | None = None
    sensor_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=160)
    tag: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    data_type: SignalDataType | None = None
    direction: SignalDirection | None = None
    engineering_unit: str | None = Field(default=None, max_length=40)
    min_value: float | None = None
    max_value: float | None = None
    current_value: dict[str, Any] | None = None
    quality: str | None = Field(default=None, max_length=40)
    source_address: str | None = Field(default=None, max_length=255)
    scan_rate_ms: int | None = Field(default=None, gt=0)
    is_writable: bool | None = None
    metadata_json: dict[str, Any] | None = None


class SignalRead(SignalBase, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class AlarmBase(BaseModel):
    signal_id: UUID
    code: str = Field(min_length=1, max_length=120)
    name: str = Field(min_length=1, max_length=160)
    description: str | None = None
    severity: AlarmSeverity
    state: AlarmState = AlarmState.NORMAL
    condition_expression: str = Field(min_length=1)
    setpoint: float | None = None
    deadband: float | None = Field(default=None, ge=0)
    delay_ms: int = Field(default=0, ge=0)
    is_enabled: bool = True
    requires_ack: bool = True
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class AlarmCreate(AlarmBase):
    pass


class AlarmUpdate(BaseModel):
    signal_id: UUID | None = None
    code: str | None = Field(default=None, min_length=1, max_length=120)
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    severity: AlarmSeverity | None = None
    state: AlarmState | None = None
    condition_expression: str | None = Field(default=None, min_length=1)
    setpoint: float | None = None
    deadband: float | None = Field(default=None, ge=0)
    delay_ms: int | None = Field(default=None, ge=0)
    is_enabled: bool | None = None
    requires_ack: bool | None = None
    metadata_json: dict[str, Any] | None = None


class AlarmRead(AlarmBase, ORMModel):
    id: UUID
    active_at: datetime | None
    acknowledged_at: datetime | None
    cleared_at: datetime | None
    created_at: datetime
    updated_at: datetime


class AlarmHistoryBase(BaseModel):
    alarm_id: UUID
    actor_id: UUID | None = None
    event_type: AlarmHistoryEventType
    previous_state: AlarmState | None = None
    new_state: AlarmState | None = None
    value_snapshot: dict[str, Any] | None = None
    message: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class AlarmHistoryCreate(AlarmHistoryBase):
    pass


class AlarmHistoryRead(AlarmHistoryBase, ORMModel):
    id: UUID
    occurred_at: datetime


class TemplateCategoryBase(BaseModel):
    parent_id: UUID | None = None
    name: str = Field(min_length=1, max_length=120)
    slug: str = Field(min_length=1, max_length=120)
    description: str | None = None
    sort_order: int = 0


class TemplateCategoryCreate(TemplateCategoryBase):
    pass


class TemplateCategoryUpdate(BaseModel):
    parent_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=120)
    slug: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    sort_order: int | None = None


class TemplateCategoryRead(TemplateCategoryBase, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class TemplateBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    category_id: UUID
    name: str = Field(min_length=1, max_length=160)
    slug: str = Field(min_length=1, max_length=160)
    industry: str = Field(default="general", min_length=1, max_length=120)
    description: str | None = None
    layout: dict[str, Any] = Field(default_factory=dict)
    components: list[dict[str, Any]] = Field(default_factory=list)
    template_schema: dict[str, Any] | None = Field(default=None, alias="schema_json")
    preview_image_url: str | None = Field(default=None, max_length=500)
    version: int = Field(default=1, gt=0)
    is_active: bool = True
    metadata_json: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_template_structure(self) -> "TemplateBase":
        if not isinstance(self.layout, dict):
            raise ValueError("Template layout must be an object.")
        if not isinstance(self.components, list):
            raise ValueError("Template components must be an array.")
        return self


class TemplateCreate(TemplateBase):
    pass


class TemplateUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    category_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=160)
    slug: str | None = Field(default=None, min_length=1, max_length=160)
    industry: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    layout: dict[str, Any] | None = None
    components: list[dict[str, Any]] | None = None
    template_schema: dict[str, Any] | None = Field(default=None, alias="schema_json")
    preview_image_url: str | None = Field(default=None, max_length=500)
    version: int | None = Field(default=None, gt=0)
    is_active: bool | None = None
    metadata_json: dict[str, Any] | None = None

    @model_validator(mode="after")
    def validate_template_update_structure(self) -> "TemplateUpdate":
        if self.layout is not None and not isinstance(self.layout, dict):
            raise ValueError("Template layout must be an object.")
        if self.components is not None and not isinstance(self.components, list):
            raise ValueError("Template components must be an array.")
        return self


class TemplateRead(TemplateBase, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    category: TemplateCategoryRead | None = None


class TemplateCloneRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    slug: str | None = Field(default=None, min_length=1, max_length=160)
    category_id: UUID | None = None


class TemplateSearchParams(BaseModel):
    q: str | None = None
    industry: str | None = None
    category_id: UUID | None = None
    is_active: bool | None = True


class DashboardBase(BaseModel):
    owner_id: UUID
    industrial_system_id: UUID | None = None
    template_id: UUID | None = None
    name: str = Field(min_length=1, max_length=160)
    slug: str = Field(min_length=1, max_length=160)
    description: str | None = None
    status: DashboardStatus = DashboardStatus.DRAFT
    schema_version: int = Field(default=1, gt=0)
    is_public: bool = False
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class DashboardCreate(DashboardBase):
    pass


class DashboardUpdate(BaseModel):
    owner_id: UUID | None = None
    industrial_system_id: UUID | None = None
    template_id: UUID | None = None
    name: str | None = Field(default=None, min_length=1, max_length=160)
    slug: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    status: DashboardStatus | None = None
    schema_version: int | None = Field(default=None, gt=0)
    is_public: bool | None = None
    published_at: datetime | None = None
    metadata_json: dict[str, Any] | None = None


class DashboardRead(DashboardBase, ORMModel):
    id: UUID
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime


class DashboardLayoutBase(BaseModel):
    dashboard_id: UUID
    breakpoint: str = Field(min_length=1, max_length=40)
    columns: int = Field(gt=0)
    row_height: int = Field(gt=0)
    layout_json: dict[str, Any]


class DashboardLayoutCreate(DashboardLayoutBase):
    pass


class DashboardLayoutUpdate(BaseModel):
    breakpoint: str | None = Field(default=None, min_length=1, max_length=40)
    columns: int | None = Field(default=None, gt=0)
    row_height: int | None = Field(default=None, gt=0)
    layout_json: dict[str, Any] | None = None


class DashboardLayoutRead(DashboardLayoutBase, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class DashboardEditorLayout(BaseModel):
    breakpoint: str = Field(default='lg', min_length=1, max_length=40)
    columns: int = Field(default=12, gt=0)
    row_height: int = Field(default=30, gt=0)
    components: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DashboardEditorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str | None = None
    metadata_id: UUID | None = None
    template_id: UUID | None = None
    status: DashboardStatus = DashboardStatus.DRAFT
    schema_version: int = Field(default=1, gt=0)
    is_public: bool = False
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    layout: DashboardEditorLayout | None = None


class DashboardEditorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = None
    metadata_id: UUID | None = None
    template_id: UUID | None = None
    status: DashboardStatus | None = None
    schema_version: int | None = Field(default=None, gt=0)
    is_public: bool | None = None
    metadata_json: dict[str, Any] | None = None
    layout: DashboardEditorLayout | None = None


class DashboardEditorRead(BaseModel):
    dashboard: DashboardRead
    layout: DashboardLayoutRead | None = None


class ComponentBase(BaseModel):
    dashboard_id: UUID
    signal_id: UUID | None = None
    parent_component_id: UUID | None = None
    component_key: str = Field(min_length=2, max_length=120)
    type: str = Field(min_length=1, max_length=120)
    kind: ComponentKind
    title: str | None = Field(default=None, max_length=160)
    props_json: dict[str, Any] = Field(default_factory=dict)
    style_json: dict[str, Any] = Field(default_factory=dict)
    binding_json: dict[str, Any] = Field(default_factory=dict)
    interaction_json: dict[str, Any] = Field(default_factory=dict)
    visibility_json: dict[str, Any] = Field(default_factory=dict)
    registry_version: str = Field(default="1.0.0", max_length=40)
    sort_order: int = 0


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    signal_id: UUID | None = None
    parent_component_id: UUID | None = None
    component_key: str | None = Field(default=None, min_length=2, max_length=120)
    type: str | None = Field(default=None, min_length=1, max_length=120)
    kind: ComponentKind | None = None
    title: str | None = Field(default=None, max_length=160)
    props_json: dict[str, Any] | None = None
    style_json: dict[str, Any] | None = None
    binding_json: dict[str, Any] | None = None
    interaction_json: dict[str, Any] | None = None
    visibility_json: dict[str, Any] | None = None
    registry_version: str | None = Field(default=None, max_length=40)
    sort_order: int | None = None


class ComponentRead(ComponentBase, ORMModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


class AssistantLogBase(BaseModel):
    user_id: UUID | None = None
    dashboard_id: UUID | None = None
    log_type: AssistantLogType
    prompt: str | None = None
    response: str | None = None
    request_json: dict[str, Any] | None = None
    response_json: dict[str, Any] | None = None
    model_name: str | None = Field(default=None, max_length=120)
    status: str = Field(default="completed", max_length=40)
    latency_ms: int | None = Field(default=None, ge=0)


class AssistantLogCreate(AssistantLogBase):
    pass


class AssistantLogRead(AssistantLogBase, ORMModel):
    id: UUID
    created_at: datetime


class MetadataSensorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    code: str = Field(min_length=2, max_length=120)
    sensor_type: str = Field(min_length=1, max_length=80)
    manufacturer: str | None = Field(default=None, max_length=120)
    model: str | None = Field(default=None, max_length=120)
    serial_number: str | None = Field(default=None, max_length=120)
    location: str | None = Field(default=None, max_length=160)
    status: SensorStatus = SensorStatus.ACTIVE
    calibration_due_at: datetime | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class MetadataAlarmThresholdCreate(BaseModel):
    code: str = Field(min_length=1, max_length=120)
    name: str = Field(min_length=1, max_length=160)
    description: str | None = None
    severity: AlarmSeverity
    criticality_level: int = Field(ge=1, le=5)
    condition_expression: str = Field(min_length=1)
    setpoint: float | None = None
    deadband: float | None = Field(default=None, ge=0)
    delay_ms: int = Field(default=0, ge=0)
    is_enabled: bool = True
    requires_ack: bool = True
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class MetadataSignalCreate(BaseModel):
    sensor_code: str | None = Field(default=None, min_length=2, max_length=120)
    name: str = Field(min_length=1, max_length=160)
    tag: str = Field(min_length=1, max_length=160)
    description: str | None = None
    data_type: SignalDataType
    direction: SignalDirection
    engineering_unit: str | None = Field(default=None, max_length=40)
    min_value: float | None = None
    max_value: float | None = None
    source_address: str | None = Field(default=None, max_length=255)
    scan_rate_ms: int = Field(default=1000, gt=0)
    is_writable: bool = False
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    alarm_thresholds: list[MetadataAlarmThresholdCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_signal_range(self) -> "MetadataSignalCreate":
        if (
            self.min_value is not None
            and self.max_value is not None
            and self.min_value > self.max_value
        ):
            raise ValueError("Signal min_value cannot be greater than max_value.")
        for alarm in self.alarm_thresholds:
            if (
                alarm.setpoint is not None
                and self.min_value is not None
                and alarm.setpoint < self.min_value
            ):
                raise ValueError("Alarm setpoint cannot be below signal min_value.")
            if (
                alarm.setpoint is not None
                and self.max_value is not None
                and alarm.setpoint > self.max_value
            ):
                raise ValueError("Alarm setpoint cannot be above signal max_value.")
        return self


class MetadataCreate(BaseModel):
    industrial_system: IndustrialSystemCreate
    sensors: list[MetadataSensorCreate] = Field(default_factory=list)
    signals: list[MetadataSignalCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_payload_keys(self) -> "MetadataCreate":
        sensor_codes = [sensor.code for sensor in self.sensors]
        signal_tags = [signal.tag for signal in self.signals]
        alarm_codes = [
            alarm.code
            for signal in self.signals
            for alarm in signal.alarm_thresholds
        ]
        if len(sensor_codes) != len(set(sensor_codes)):
            raise ValueError("Sensor codes must be unique within a metadata payload.")
        if len(signal_tags) != len(set(signal_tags)):
            raise ValueError("Signal tags must be unique within a metadata payload.")
        if len(alarm_codes) != len(set(alarm_codes)):
            raise ValueError("Alarm codes must be unique within a metadata payload.")

        known_sensor_codes = set(sensor_codes)
        for signal in self.signals:
            if signal.sensor_code and signal.sensor_code not in known_sensor_codes:
                raise ValueError(
                    f"Signal references unknown sensor_code: {signal.sensor_code}."
                )
        return self


class MetadataUpdate(BaseModel):
    industrial_system: IndustrialSystemUpdate | None = None
    sensors: list[MetadataSensorCreate] | None = None
    signals: list[MetadataSignalCreate] | None = None

    @model_validator(mode="after")
    def validate_unique_payload_keys(self) -> "MetadataUpdate":
        sensor_codes = [sensor.code for sensor in self.sensors or []]
        signal_tags = [signal.tag for signal in self.signals or []]
        alarm_codes = [
            alarm.code
            for signal in self.signals or []
            for alarm in signal.alarm_thresholds
        ]
        if len(sensor_codes) != len(set(sensor_codes)):
            raise ValueError("Sensor codes must be unique within a metadata payload.")
        if len(signal_tags) != len(set(signal_tags)):
            raise ValueError("Signal tags must be unique within a metadata payload.")
        if len(alarm_codes) != len(set(alarm_codes)):
            raise ValueError("Alarm codes must be unique within a metadata payload.")

        known_sensor_codes = set(sensor_codes)
        if self.sensors is not None and self.signals is not None:
            for signal in self.signals:
                if signal.sensor_code and signal.sensor_code not in known_sensor_codes:
                    raise ValueError(
                        f"Signal references unknown sensor_code: {signal.sensor_code}."
                    )
        return self


class MetadataRead(ORMModel):
    industrial_system: IndustrialSystemRead
    sensors: list[SensorRead]
    signals: list[SignalRead]
    alarms: list[AlarmRead]


class AlarmStreamEvent(BaseModel):
    code: str = Field(min_length=1, max_length=120)
    name: str | None = Field(default=None, max_length=160)
    severity: AlarmSeverity | str = AlarmSeverity.MEDIUM
    source: str | None = Field(default=None, max_length=160)
    source_name: str | None = Field(default=None, max_length=160)
    signal_tag: str | None = Field(default=None, max_length=160)
    signal: str | None = Field(default=None, max_length=160)
    message: str | None = None
    timestamp: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    metadata_json: dict[str, Any] | None = None


class AlarmIntelligenceRequest(BaseModel):
    events: list[AlarmStreamEvent] = Field(min_length=1)


class AlarmIntelligenceGroup(BaseModel):
    key: str
    alarm_count: int = Field(ge=0)
    max_severity: str
    affected_signals: list[str] = Field(default_factory=list)


class AlarmIntelligenceCluster(BaseModel):
    cluster_id: int
    alarm_count: int = Field(ge=0)
    average_severity: str
    representative_signal: str | None = None


class AlarmIntelligenceAnalysis(BaseModel):
    root_cause: str
    confidence: int = Field(ge=0, le=100)
    affected_signals: list[str] = Field(default_factory=list)
    severity_ranking: list[dict[str, Any]] = Field(default_factory=list)
    suppressed_duplicates: int = Field(ge=0)
    grouped_incidents: list[AlarmIntelligenceGroup] = Field(default_factory=list)
    incident_clusters: list[AlarmIntelligenceCluster] = Field(default_factory=list)


class AlarmIntelligenceResultRead(AlarmIntelligenceAnalysis, ORMModel):
    id: UUID
    input_event_count: int = Field(ge=0)
    created_at: datetime
