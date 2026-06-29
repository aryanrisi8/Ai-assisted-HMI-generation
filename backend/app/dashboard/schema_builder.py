"""JSON Schema Builder for Dashboard Output."""

from datetime import datetime
from typing import Any

from app.dashboard.schemas import DashboardComponent, LayoutSchema


class JsonSchemaBuilder:
    """
    Builds the output JSON schema for the dashboard.

    Converts internal component representations into the final
    JSON layout schema format.
    """

    def __init__(self) -> None:
        """Initialize the schema builder."""
        self.version = "1.0"

    def build(
        self,
        components: list[DashboardComponent],
        layout_metadata: dict[str, Any] | None = None,
    ) -> LayoutSchema:
        """
        Build the final layout schema.

        Args:
            components: List of positioned components.
            layout_metadata: Optional layout metadata.

        Returns:
            Complete layout schema.
        """
        if layout_metadata is None:
            layout_metadata = self._default_layout_metadata()

        return LayoutSchema(
            layout=layout_metadata,
            components=components,
            created_at=datetime.utcnow(),
            version=self.version,
        )

    def build_json(
        self,
        components: list[DashboardComponent],
        layout_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build and serialize to JSON dict.

        Args:
            components: List of positioned components.
            layout_metadata: Optional layout metadata.

        Returns:
            JSON-serializable dictionary.
        """
        schema = self.build(components, layout_metadata)
        return self._schema_to_json(schema)

    def _schema_to_json(self, schema: LayoutSchema) -> dict[str, Any]:
        """
        Convert schema to JSON dictionary.

        Args:
            schema: Layout schema.

        Returns:
            JSON dictionary.
        """
        return {
            "layout": schema.layout,
            "components": [
                self._component_to_json(comp) for comp in schema.components
            ],
            "metadata": {
                "created_at": schema.created_at.isoformat() if schema.created_at else None,
                "version": schema.version,
                "component_count": len(schema.components),
            },
        }

    def _component_to_json(self, component: DashboardComponent) -> dict[str, Any]:
        """
        Convert component to JSON.

        Args:
            component: Dashboard component.

        Returns:
            JSON dictionary.
        """
        return {
            "component": {
                "type": component.component.type.value,
                "title": component.component.title,
                "bindings": [
                    self._binding_to_json(binding)
                    for binding in component.component.bindings
                ],
                "properties": component.component.properties,
                "refresh_interval": component.component.refresh_interval,
            },
            "position": {
                "row": component.position.row,
                "col": component.position.col,
                "width": component.position.width,
                "height": component.position.height,
            },
        }

    @staticmethod
    def _binding_to_json(binding: Any) -> dict[str, Any]:
        """
        Convert binding to JSON.

        Args:
            binding: Component binding.

        Returns:
            JSON dictionary.
        """
        return {
            "source_type": binding.source_type.value,
            "source_id": binding.source_id,
            "source_tag": binding.source_tag,
            "property_name": binding.property_name,
        }

    @staticmethod
    def _default_layout_metadata() -> dict[str, Any]:
        """Create default layout metadata."""
        return {
            "grid_width": 12,
            "grid_height": 20,
            "spacing": 12,
            "theme": "light",
            "responsive": True,
            "grid_unit": "px",
        }

    def build_with_metrics(
        self,
        components: list[DashboardComponent],
        metrics: dict[str, Any],
        layout_metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build schema with layout metrics.

        Args:
            components: List of positioned components.
            metrics: Layout metrics from generator.
            layout_metadata: Optional layout metadata.

        Returns:
            JSON with metrics included.
        """
        json_output = self.build_json(components, layout_metadata)
        json_output["metrics"] = metrics
        return json_output

    def add_theme(
        self,
        json_output: dict[str, Any],
        theme_name: str = "light",
        custom_theme: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Add theme configuration to output.

        Args:
            json_output: JSON output.
            theme_name: Theme name.
            custom_theme: Custom theme configuration.

        Returns:
            Updated JSON output.
        """
        themes = {
            "light": {
                "primary": "#2196F3",
                "secondary": "#757575",
                "background": "#FAFAFA",
                "surface": "#FFFFFF",
                "error": "#F44336",
            },
            "dark": {
                "primary": "#90CAF9",
                "secondary": "#B0B0B0",
                "background": "#121212",
                "surface": "#1E1E1E",
                "error": "#CF6679",
            },
        }

        theme = custom_theme or themes.get(theme_name, themes["light"])
        json_output["theme"] = {
            "name": theme_name,
            "colors": theme,
        }

        return json_output

    def add_interactions(
        self,
        json_output: dict[str, Any],
        interactions: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Add interaction configuration.

        Args:
            json_output: JSON output.
            interactions: List of interaction configs.

        Returns:
            Updated JSON output.
        """
        if interactions is None:
            interactions = self._default_interactions()

        json_output["interactions"] = interactions
        return json_output

    @staticmethod
    def _default_interactions() -> list[dict[str, Any]]:
        """Create default interactions."""
        return [
            {
                "event": "component_click",
                "actions": ["drill_down", "show_details", "export"],
            },
            {
                "event": "time_range_change",
                "actions": ["refresh_all", "update_metrics"],
            },
            {
                "event": "filter_change",
                "actions": ["refresh_affected", "update_aggregate"],
            },
        ]

    def build_minimal_schema(
        self,
        components: list[DashboardComponent],
    ) -> dict[str, Any]:
        """
        Build minimal schema (matching example format).

        Args:
            components: List of components.

        Returns:
            Minimal JSON schema.
        """
        return {
            "layout": self._default_layout_metadata(),
            "components": [
                self._component_to_json(comp) for comp in components
            ],
        }
