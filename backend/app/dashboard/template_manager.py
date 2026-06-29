"""Template Manager for Dashboard Generation."""

from app.dashboard.schemas import (
    ComponentConfig,
    ComponentType,
    DataSourceType,
    IndustrialSystemMetadata,
    TemplateDefinition,
)


class TemplateManager:
    """
    Manages dashboard templates.

    Stores, retrieves, and matches templates against industrial metadata.
    """

    def __init__(self) -> None:
        """Initialize the template manager."""
        self.templates: dict[str, TemplateDefinition] = {}
        self._initialize_default_templates()

    def _initialize_default_templates(self) -> None:
        """Initialize default templates for common use cases."""

        # Template 1: Simple monitoring system (few sensors)
        simple_template = TemplateDefinition(
            id="simple_monitoring",
            name="Simple Monitoring Dashboard",
            description="Basic dashboard for systems with 1-3 sensors",
            applies_to={"sensor_count": {"min": 1, "max": 3}, "signal_count": {"min": 1, "max": 10}},
            layout_config={
                "grid_width": 12,
                "grid_height": 8,
                "spacing": 16,
                "theme": "light",
            },
            component_templates=[
                ComponentConfig(
                    type=ComponentType.STAT_CARD,
                    title="Primary Metric",
                    bindings=[],
                    properties={"size": "large", "show_history": True},
                ),
                ComponentConfig(
                    type=ComponentType.GAUGE,
                    title="Gauge",
                    bindings=[],
                    properties={"show_thresholds": True},
                ),
            ],
            priority=10,
        )
        self.templates["simple_monitoring"] = simple_template

        # Template 2: Multi-sensor monitoring
        multi_template = TemplateDefinition(
            id="multi_sensor",
            name="Multi-Sensor Monitoring",
            description="Dashboard for systems with multiple sensors",
            applies_to={"sensor_count": {"min": 4, "max": 20}, "signal_count": {"min": 10, "max": 50}},
            layout_config={
                "grid_width": 12,
                "grid_height": 12,
                "spacing": 12,
                "theme": "light",
            },
            component_templates=[
                ComponentConfig(
                    type=ComponentType.STAT_CARD,
                    title="Overview",
                    bindings=[],
                    properties={"highlight_top": 3},
                ),
                ComponentConfig(
                    type=ComponentType.LINE_CHART,
                    title="Trends",
                    bindings=[],
                    properties={"time_window": "1h", "aggregate": "average"},
                ),
                ComponentConfig(
                    type=ComponentType.TABLE,
                    title="All Signals",
                    bindings=[],
                    properties={"sortable": True, "filterable": True},
                ),
            ],
            priority=5,
        )
        self.templates["multi_sensor"] = multi_template

        # Template 3: Alarm-heavy system
        alarm_template = TemplateDefinition(
            id="alarm_monitoring",
            name="Alarm Monitoring Dashboard",
            description="Dashboard focused on alarm management",
            applies_to={"has_alarms": True, "alarm_count": {"min": 1}},
            layout_config={
                "grid_width": 12,
                "grid_height": 10,
                "spacing": 12,
                "theme": "dark",
            },
            component_templates=[
                ComponentConfig(
                    type=ComponentType.ALARM_PANEL,
                    title="Active Alarms",
                    bindings=[],
                    properties={
                        "show_severity": True,
                        "auto_refresh": True,
                        "highlight_critical": True,
                    },
                ),
                ComponentConfig(
                    type=ComponentType.STAT_CARD,
                    title="System Health",
                    bindings=[],
                    properties={"show_status": True},
                ),
            ],
            priority=15,
        )
        self.templates["alarm_monitoring"] = alarm_template

        # Template 4: Complex industrial system
        complex_template = TemplateDefinition(
            id="complex_industrial",
            name="Complex Industrial System",
            description="Comprehensive dashboard for large industrial systems",
            applies_to={"sensor_count": {"min": 20}, "signal_count": {"min": 50}},
            layout_config={
                "grid_width": 24,
                "grid_height": 16,
                "spacing": 8,
                "theme": "light",
                "multi_page": True,
            },
            component_templates=[
                ComponentConfig(
                    type=ComponentType.STAT_CARD,
                    title="KPIs",
                    bindings=[],
                    properties={"layout": "grid", "columns": 4},
                ),
                ComponentConfig(
                    type=ComponentType.LINE_CHART,
                    title="Production Metrics",
                    bindings=[],
                    properties={"time_window": "24h"},
                ),
                ComponentConfig(
                    type=ComponentType.HEATMAP,
                    title="System Status Matrix",
                    bindings=[],
                    properties={"show_legend": True},
                ),
                ComponentConfig(
                    type=ComponentType.TABLE,
                    title="Detailed Signals",
                    bindings=[],
                    properties={"pagination": 20},
                ),
            ],
            priority=1,
        )
        self.templates["complex_industrial"] = complex_template

    def find_matching_templates(self, metadata: IndustrialSystemMetadata) -> list[TemplateDefinition]:
        """
        Find templates that match the given metadata.

        Args:
            metadata: Industrial system metadata.

        Returns:
            List of matching templates sorted by priority.
        """
        matching = []
        context = self._build_matching_context(metadata)

        for template in self.templates.values():
            if self._matches_criteria(template.applies_to, context):
                matching.append(template)

        # Sort by priority (higher priority first)
        return sorted(matching, key=lambda t: t.priority, reverse=True)

    def get_template(self, template_id: str) -> TemplateDefinition | None:
        """
        Get a template by ID.

        Args:
            template_id: Template ID.

        Returns:
            Template or None if not found.
        """
        return self.templates.get(template_id)

    def register_template(self, template: TemplateDefinition) -> None:
        """
        Register a new template.

        Args:
            template: Template definition.
        """
        self.templates[template.id] = template

    def _build_matching_context(self, metadata: IndustrialSystemMetadata) -> dict:
        """Build context for template matching."""
        sensor_count = len(metadata.sensors)
        signal_count = sum(len(sensor.signals) for sensor in metadata.sensors)

        return {
            "sensor_count": sensor_count,
            "signal_count": signal_count,
            "has_alarms": len(metadata.alarms) > 0,
            "alarm_count": len(metadata.alarms),
            "system_type": metadata.system_type,
        }

    def _matches_criteria(self, criteria: dict, context: dict) -> bool:
        """
        Check if context matches template criteria.

        Args:
            criteria: Template matching criteria.
            context: System context.

        Returns:
            True if all criteria match.
        """
        for key, value in criteria.items():
            if key not in context:
                continue

            context_value = context[key]

            # Handle boolean checks
            if isinstance(value, bool):
                if context_value != value:
                    return False

            # Handle range checks
            elif isinstance(value, dict):
                if "min" in value and context_value < value["min"]:
                    return False
                if "max" in value and context_value > value["max"]:
                    return False

            # Handle direct equality
            else:
                if context_value != value:
                    return False

        return True

    def get_all_templates(self) -> list[TemplateDefinition]:
        """Get all registered templates."""
        return list(self.templates.values())

    def clear_custom_templates(self) -> None:
        """Clear custom templates, keeping defaults."""
        default_ids = {
            "simple_monitoring",
            "multi_sensor",
            "alarm_monitoring",
            "complex_industrial",
        }
        to_remove = [tid for tid in self.templates.keys() if tid not in default_ids]
        for tid in to_remove:
            del self.templates[tid]
