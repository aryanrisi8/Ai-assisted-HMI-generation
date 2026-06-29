"""Dashboard Generation Schemas and Models."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ComponentType(str, Enum):
    """Supported component types for dashboard."""

    GAUGE = "gauge"
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    TABLE = "table"
    STAT_CARD = "stat_card"
    ALARM_PANEL = "alarm_panel"
    INDICATOR = "indicator"
    TREND = "trend"
    HEATMAP = "heatmap"


class DataSourceType(str, Enum):
    """Data source types."""

    SIGNAL = "signal"
    SENSOR = "sensor"
    SYSTEM = "system"
    ALARM = "alarm"


class LayoutPosition(BaseModel):
    """Position in the dashboard grid."""

    row: int = Field(ge=0, description="Row position (0-based)")
    col: int = Field(ge=0, description="Column position (0-based)")
    width: int = Field(default=4, ge=1, le=12, description="Width in grid units")
    height: int = Field(default=4, ge=1, le=12, description="Height in grid units")


class ComponentBinding(BaseModel):
    """Binding configuration for a component."""

    source_type: DataSourceType
    source_id: str | None = None
    source_tag: str | None = None
    property_name: str | None = None


class ComponentConfig(BaseModel):
    """Component configuration."""

    type: ComponentType
    title: str
    bindings: list[ComponentBinding]
    properties: dict[str, Any] = Field(default_factory=dict)
    refresh_interval: int | None = Field(default=5, ge=1, description="Refresh interval in seconds")


class DashboardComponent(BaseModel):
    """Component with its layout position."""

    component: ComponentConfig
    position: LayoutPosition


class LayoutSchema(BaseModel):
    """Complete dashboard layout schema."""

    layout: dict[str, Any] = Field(default_factory=dict, description="Layout metadata")
    components: list[DashboardComponent]
    created_at: datetime | None = None
    version: str = "1.0"


# Input Schema


class IndustrialSignalMetadata(BaseModel):
    """Signal metadata from industrial system."""

    id: str
    tag: str
    name: str
    data_type: str
    direction: str
    unit: str | None = None
    min_value: float | None = None
    max_value: float | None = None
    description: str | None = None


class IndustrialSensorMetadata(BaseModel):
    """Sensor metadata from industrial system."""

    id: str
    code: str
    name: str
    sensor_type: str
    description: str | None = None
    signals: list[IndustrialSignalMetadata]


class IndustrialSystemMetadata(BaseModel):
    """Industrial system metadata."""

    id: UUID | str
    name: str
    code: str
    description: str | None = None
    system_type: str | None = None
    location: str | None = None
    sensors: list[IndustrialSensorMetadata]
    alarms: list[dict[str, Any]] = Field(default_factory=list)


# Rule Engine


class Rule(BaseModel):
    """Rule definition for dashboard generation."""

    id: str
    name: str
    description: str | None = None
    conditions: dict[str, Any]
    actions: dict[str, Any]
    priority: int = Field(default=0, ge=0)
    enabled: bool = True


class RuleContext(BaseModel):
    """Context passed to rules engine."""

    metadata: IndustrialSystemMetadata
    signal_count: int = 0
    sensor_count: int = 0
    has_alarms: bool = False
    system_type: str | None = None
    signal_types: set[str] = Field(default_factory=set)


class RuleResult(BaseModel):
    """Result from rule evaluation."""

    rule_id: str
    matched: bool
    actions: dict[str, Any]


# Template


class TemplateDefinition(BaseModel):
    """Template definition for dashboard generation."""

    id: str
    name: str
    description: str | None = None
    version: str = "1.0"
    applies_to: dict[str, Any]  # Matching criteria
    layout_config: dict[str, Any]  # Layout metadata
    component_templates: list[ComponentConfig]
    priority: int = Field(default=0, ge=0)


# Component Recommendation


class ComponentRecommendation(BaseModel):
    """Component recommendation with reasoning."""

    component_type: ComponentType
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)
    source_bindings: list[ComponentBinding]
    suggested_properties: dict[str, Any] = Field(default_factory=dict)


class RecommendationResult(BaseModel):
    """Result with component recommendations."""

    recommendations: list[ComponentRecommendation]
    layout_reasoning: str
    estimated_grid_size: dict[str, int]  # width, height
