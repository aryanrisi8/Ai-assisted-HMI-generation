"""Dashboard Generation Service."""

from typing import Any

from app.dashboard.components import ComponentRecommendationEngine
from app.dashboard.layout_generator import LayoutGenerator
from app.dashboard.rules_engine import RulesEngine
from app.dashboard.schemas import (
    DashboardComponent,
    IndustrialSystemMetadata,
    LayoutSchema,
    RecommendationResult,
    Rule,
    RuleContext,
)
from app.dashboard.schema_builder import JsonSchemaBuilder
from app.dashboard.template_manager import TemplateManager


class DashboardGenerationService:
    """
    Main service for dashboard generation from industrial metadata.

    Orchestrates all components: rules engine, templates, recommendations,
    layout generation, and schema building.
    """

    def __init__(self) -> None:
        """Initialize the dashboard generation service."""
        self.rules_engine = RulesEngine()
        self.template_manager = TemplateManager()
        self.recommendation_engine = ComponentRecommendationEngine()
        self.layout_generator = LayoutGenerator()
        self.schema_builder = JsonSchemaBuilder()

    def generate(
        self,
        metadata: IndustrialSystemMetadata,
        apply_rules: bool = True,
        apply_templates: bool = True,
    ) -> dict[str, Any]:
        """
        Generate complete dashboard layout schema from industrial metadata.

        Args:
            metadata: Industrial system metadata.
            apply_rules: Whether to apply rules engine.
            apply_templates: Whether to apply templates.

        Returns:
            Generated dashboard JSON schema.
        """
        # Step 1: Build rule context and apply rules if enabled
        rule_context = self._build_rule_context(metadata)
        matched_rules = []
        if apply_rules:
            matched_rules = self.rules_engine.get_matched_rules(rule_context)

        # Step 2: Find matching templates
        matching_templates = []
        if apply_templates:
            matching_templates = self.template_manager.find_matching_templates(metadata)

        # Step 3: Generate component recommendations
        recommendations = self.recommendation_engine.recommend(metadata)

        # Step 4: Generate layout
        components = self.layout_generator.generate_layout(
            recommendations.recommendations,
            template=matching_templates[0] if matching_templates else None,
        )

        # Step 5: Optimize layout
        optimized_components = self.layout_generator.optimize_layout(components)

        # Step 6: Build output schema
        layout_metadata = self._build_layout_metadata(
            metadata,
            matching_templates[0] if matching_templates else None,
        )

        output_json = self.schema_builder.build_json(optimized_components, layout_metadata)

        # Add metrics
        metrics = self.layout_generator.calculate_layout_metrics(optimized_components)
        output_json["metrics"] = metrics

        # Add generation context
        output_json["generation_context"] = {
            "rules_applied": len(matched_rules),
            "template_matched": matching_templates[0].id if matching_templates else None,
            "recommendations_count": len(recommendations.recommendations),
            "layout_reasoning": recommendations.layout_reasoning,
        }

        return output_json

    def generate_with_custom_rules(
        self,
        metadata: IndustrialSystemMetadata,
        custom_rules: list[Rule] | None = None,
    ) -> dict[str, Any]:
        """
        Generate dashboard with custom rules.

        Args:
            metadata: Industrial system metadata.
            custom_rules: List of custom rules to apply.

        Returns:
            Generated dashboard JSON schema.
        """
        if custom_rules:
            self.rules_engine.clear_rules()
            self.rules_engine.add_rules(custom_rules)

        return self.generate(metadata)

    def get_raw_recommendations(
        self,
        metadata: IndustrialSystemMetadata,
    ) -> RecommendationResult:
        """
        Get raw recommendations without layout generation.

        Args:
            metadata: Industrial system metadata.

        Returns:
            Recommendation result.
        """
        return self.recommendation_engine.recommend(metadata)

    def get_matched_templates(
        self,
        metadata: IndustrialSystemMetadata,
    ) -> list[str]:
        """
        Get IDs of templates matching the metadata.

        Args:
            metadata: Industrial system metadata.

        Returns:
            List of matching template IDs.
        """
        templates = self.template_manager.find_matching_templates(metadata)
        return [t.id for t in templates]

    def get_generated_layout(
        self,
        metadata: IndustrialSystemMetadata,
    ) -> list[DashboardComponent]:
        """
        Get generated layout components before schema building.

        Args:
            metadata: Industrial system metadata.

        Returns:
            List of positioned dashboard components.
        """
        recommendations = self.recommendation_engine.recommend(metadata)
        return self.layout_generator.generate_layout(
            recommendations.recommendations
        )

    def _build_rule_context(self, metadata: IndustrialSystemMetadata) -> RuleContext:
        """Build rule context from metadata."""
        signal_count = sum(len(sensor.signals) for sensor in metadata.sensors)
        signal_types = set()

        for sensor in metadata.sensors:
            for signal in sensor.signals:
                signal_types.add(signal.data_type.lower())

        return RuleContext(
            metadata=metadata,
            signal_count=signal_count,
            sensor_count=len(metadata.sensors),
            has_alarms=len(metadata.alarms) > 0,
            system_type=metadata.system_type,
            signal_types=signal_types,
        )

    @staticmethod
    def _build_layout_metadata(
        metadata: IndustrialSystemMetadata,
        template=None,
    ) -> dict[str, Any]:
        """Build layout metadata."""
        base_metadata = {
            "grid_width": 12,
            "grid_height": 20,
            "spacing": 12,
            "theme": "light",
            "responsive": True,
        }

        if template:
            base_metadata.update(template.layout_config)

        # Add system info
        base_metadata["system_info"] = {
            "name": metadata.name,
            "code": metadata.code,
            "type": metadata.system_type,
            "location": metadata.location,
            "sensor_count": len(metadata.sensors),
            "signal_count": sum(len(s.signals) for s in metadata.sensors),
        }

        return base_metadata


# Convenience function for quick generation
def generate_dashboard(metadata: IndustrialSystemMetadata) -> dict[str, Any]:
    """
    Quick dashboard generation.

    Args:
        metadata: Industrial system metadata.

    Returns:
        Generated dashboard JSON schema.
    """
    service = DashboardGenerationService()
    return service.generate(metadata)
