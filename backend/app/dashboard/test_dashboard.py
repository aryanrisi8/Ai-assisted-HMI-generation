"""
Unit tests for Dashboard Generation Engine.

Tests all components:
- Rules engine
- Template manager
- Component recommendations
- Layout generation
- Schema building
"""

import pytest
from uuid import uuid4

from app.dashboard.components import ComponentRecommendationEngine
from app.dashboard.layout_generator import LayoutGenerator
from app.dashboard.rules_engine import RulesEngine
from app.dashboard.schemas import (
    ComponentType,
    IndustrialSensorMetadata,
    IndustrialSignalMetadata,
    IndustrialSystemMetadata,
    Rule,
    RuleContext,
)
from app.dashboard.schema_builder import JsonSchemaBuilder
from app.dashboard.template_manager import TemplateManager
from app.services.dashboard_service import DashboardGenerationService


# Fixtures


@pytest.fixture
def simple_metadata():
    """Create simple test metadata."""
    signal = IndustrialSignalMetadata(
        id=str(uuid4()),
        tag="TEST_SIGNAL",
        name="Test Signal",
        data_type="float",
        direction="input",
        unit="units",
        min_value=0,
        max_value=100,
    )

    sensor = IndustrialSensorMetadata(
        id=str(uuid4()),
        code="TEST_001",
        name="Test Sensor",
        sensor_type="test",
        signals=[signal],
    )

    return IndustrialSystemMetadata(
        id=uuid4(),
        name="Test System",
        code="TEST_SYS",
        system_type="test",
        sensors=[sensor],
    )


@pytest.fixture
def complex_metadata():
    """Create complex test metadata."""
    sensors = []
    for i in range(3):
        signals = []
        for j in range(5):
            signals.append(
                IndustrialSignalMetadata(
                    id=str(uuid4()),
                    tag=f"SIG_{i}_{j}",
                    name=f"Signal {i}-{j}",
                    data_type="float" if j < 3 else "boolean",
                    direction="input",
                    unit="unit",
                    min_value=0 if j < 3 else None,
                    max_value=100 if j < 3 else None,
                )
            )

        sensors.append(
            IndustrialSensorMetadata(
                id=str(uuid4()),
                code=f"SEN_{i}",
                name=f"Sensor {i}",
                sensor_type="multi",
                signals=signals,
            )
        )

    return IndustrialSystemMetadata(
        id=uuid4(),
        name="Complex System",
        code="COMPLEX_SYS",
        system_type="manufacturing",
        sensors=sensors,
        alarms=[{"id": "ALM_001", "name": "Test Alarm"}],
    )


# Rules Engine Tests


class TestRulesEngine:
    """Tests for rules engine."""

    def test_add_single_rule(self):
        """Test adding a single rule."""
        engine = RulesEngine()
        rule = Rule(id="r1", name="Test Rule", conditions={}, actions={})

        engine.add_rule(rule)
        assert "r1" in engine.rules

    def test_add_multiple_rules(self):
        """Test adding multiple rules."""
        engine = RulesEngine()
        rules = [
            Rule(id=f"r{i}", name=f"Rule {i}", conditions={}, actions={})
            for i in range(3)
        ]

        engine.add_rules(rules)
        assert len(engine.rules) == 3

    def test_disable_rule(self):
        """Test that disabled rules are not added."""
        engine = RulesEngine()
        rule = Rule(id="r1", name="Test", conditions={}, actions={}, enabled=False)

        engine.add_rule(rule)
        assert "r1" not in engine.rules

    def test_signal_count_condition(self, simple_metadata):
        """Test signal count condition."""
        engine = RulesEngine()
        context = RuleContext(metadata=simple_metadata, signal_count=1)

        # Test exact match
        assert engine._check_numeric_range(1, 1) is True
        assert engine._check_numeric_range(2, 1) is False

        # Test range
        assert engine._check_numeric_range(5, {"min": 0, "max": 10}) is True
        assert engine._check_numeric_range(15, {"min": 0, "max": 10}) is False

    def test_evaluate_conditions(self, complex_metadata):
        """Test condition evaluation."""
        engine = RulesEngine()
        context = RuleContext(
            metadata=complex_metadata,
            signal_count=15,
            sensor_count=3,
            has_alarms=True,
        )

        conditions = {
            "signal_count": {"min": 10},
            "sensor_count": 3,
            "has_alarms": True,
        }

        assert engine._evaluate_conditions(conditions, context) is True

    def test_rule_priority(self):
        """Test rule sorting by priority."""
        engine = RulesEngine()
        rules = [
            Rule(id="r1", name="Low", conditions={}, actions={}, priority=1),
            Rule(id="r2", name="High", conditions={}, actions={}, priority=10),
            Rule(id="r3", name="Medium", conditions={}, actions={}, priority=5),
        ]

        engine.add_rules(rules)
        sorted_rules = sorted(engine.rules.values(), key=lambda r: r.priority, reverse=True)

        assert sorted_rules[0].id == "r2"
        assert sorted_rules[1].id == "r3"
        assert sorted_rules[2].id == "r1"


# Template Manager Tests


class TestTemplateManager:
    """Tests for template manager."""

    def test_default_templates_loaded(self):
        """Test that default templates are initialized."""
        manager = TemplateManager()
        assert len(manager.templates) >= 4

    def test_get_template(self):
        """Test retrieving a template."""
        manager = TemplateManager()
        template = manager.get_template("simple_monitoring")
        assert template is not None
        assert template.id == "simple_monitoring"

    def test_find_matching_templates_simple(self, simple_metadata):
        """Test finding templates for simple metadata."""
        manager = TemplateManager()
        matches = manager.find_matching_templates(simple_metadata)
        assert len(matches) > 0
        assert matches[0].id == "simple_monitoring"

    def test_find_matching_templates_complex(self, complex_metadata):
        """Test finding templates for complex metadata."""
        manager = TemplateManager()
        matches = manager.find_matching_templates(complex_metadata)
        assert len(matches) > 0

    def test_register_custom_template(self):
        """Test registering custom template."""
        from app.dashboard.schemas import TemplateDefinition

        manager = TemplateManager()
        template = TemplateDefinition(
            id="custom",
            name="Custom",
            applies_to={},
            layout_config={},
            component_templates=[],
        )

        manager.register_template(template)
        assert manager.get_template("custom") is not None


# Component Recommendation Tests


class TestComponentRecommendation:
    """Tests for component recommendation engine."""

    def test_recommend_simple(self, simple_metadata):
        """Test basic recommendations."""
        engine = ComponentRecommendationEngine()
        result = engine.recommend(simple_metadata)

        assert len(result.recommendations) > 0
        assert all(r.confidence > 0 for r in result.recommendations)

    def test_recommend_complex(self, complex_metadata):
        """Test recommendations for complex system."""
        engine = ComponentRecommendationEngine()
        result = engine.recommend(complex_metadata)

        assert len(result.recommendations) > 0
        # Should have stat cards, gauges, charts
        types = {r.component_type for r in result.recommendations}
        assert ComponentType.STAT_CARD in types or ComponentType.GAUGE in types

    def test_recommendations_sorted_by_confidence(self, complex_metadata):
        """Test that recommendations are sorted by confidence."""
        engine = ComponentRecommendationEngine()
        result = engine.recommend(complex_metadata)

        confidences = [r.confidence for r in result.recommendations]
        assert confidences == sorted(confidences, reverse=True)

    def test_stat_card_recommendation(self, simple_metadata):
        """Test stat card recommendation."""
        engine = ComponentRecommendationEngine()
        result = engine.recommend(simple_metadata)

        stat_cards = [r for r in result.recommendations if r.component_type == ComponentType.STAT_CARD]
        assert len(stat_cards) > 0


# Layout Generator Tests


class TestLayoutGenerator:
    """Tests for layout generator."""

    def test_grid_initialization(self):
        """Test grid initialization."""
        gen = LayoutGenerator()
        assert len(gen.grid) == 20
        assert len(gen.grid[0]) == 12
        assert all(not cell for row in gen.grid for cell in row)

    def test_mark_grid(self):
        """Test grid marking."""
        from app.dashboard.schemas import LayoutPosition

        gen = LayoutGenerator()
        pos = LayoutPosition(row=0, col=0, width=2, height=2)

        gen._mark_grid(pos)
        assert gen.grid[0][0] is True
        assert gen.grid[1][1] is True
        assert gen.grid[0][2] is False

    def test_can_place(self):
        """Test placement checking."""
        gen = LayoutGenerator()

        # Initially can place anywhere
        assert gen._can_place(0, 0, 2, 2) is True

        # After marking, cannot place
        from app.dashboard.schemas import LayoutPosition
        pos = LayoutPosition(row=0, col=0, width=2, height=2)
        gen._mark_grid(pos)
        assert gen._can_place(0, 0, 2, 2) is False

        # Can place next to
        assert gen._can_place(0, 2, 2, 2) is True

    def test_find_position(self):
        """Test finding a position."""
        gen = LayoutGenerator()
        pos = gen._find_position(ComponentType.GAUGE)

        assert pos is not None
        assert pos.width > 0
        assert pos.height > 0

    def test_calculate_metrics(self, simple_metadata):
        """Test layout metrics calculation."""
        engine = ComponentRecommendationEngine()
        result = engine.recommend(simple_metadata)

        gen = LayoutGenerator()
        components = gen.generate_layout(result.recommendations)
        metrics = gen.calculate_layout_metrics(components)

        assert metrics["component_count"] == len(components)
        assert 0 <= metrics["utilization"] <= 100


# Schema Builder Tests


class TestJsonSchemaBuilder:
    """Tests for JSON schema builder."""

    def test_build_minimal_schema(self, simple_metadata):
        """Test building minimal schema."""
        service = DashboardGenerationService()
        layout = service.get_generated_layout(simple_metadata)

        builder = JsonSchemaBuilder()
        schema_json = builder.build_minimal_schema(layout)

        assert "layout" in schema_json
        assert "components" in schema_json
        assert len(schema_json["components"]) > 0

    def test_build_with_metadata(self, simple_metadata):
        """Test building schema with metadata."""
        service = DashboardGenerationService()
        layout = service.get_generated_layout(simple_metadata)

        builder = JsonSchemaBuilder()
        schema_json = builder.build_json(layout)

        assert "metadata" in schema_json
        assert schema_json["metadata"]["version"] == "1.0"

    def test_component_to_json(self, simple_metadata):
        """Test component conversion to JSON."""
        service = DashboardGenerationService()
        layout = service.get_generated_layout(simple_metadata)

        builder = JsonSchemaBuilder()
        comp_json = builder._component_to_json(layout[0])

        assert "component" in comp_json
        assert "position" in comp_json
        assert "type" in comp_json["component"]


# Integration Tests


class TestDashboardGenerationService:
    """Integration tests for dashboard service."""

    def test_basic_generation(self, simple_metadata):
        """Test basic generation."""
        service = DashboardGenerationService()
        result = service.generate(simple_metadata)

        assert "layout" in result
        assert "components" in result
        assert "generation_context" in result

    def test_generation_with_templates(self, complex_metadata):
        """Test generation using templates."""
        service = DashboardGenerationService()
        result = service.generate(complex_metadata, apply_templates=True)

        assert result["generation_context"]["template_matched"] is not None

    def test_generation_with_rules(self, complex_metadata):
        """Test generation with custom rules."""
        service = DashboardGenerationService()

        rules = [
            Rule(
                id="test_rule",
                name="Test",
                conditions={"sensor_count": 3},
                actions={"theme": "dark"},
                priority=10,
            )
        ]

        result = service.generate_with_custom_rules(complex_metadata, rules)
        assert result["generation_context"]["rules_applied"] >= 0

    def test_get_matched_templates(self, complex_metadata):
        """Test getting matched templates."""
        service = DashboardGenerationService()
        templates = service.get_matched_templates(complex_metadata)

        assert isinstance(templates, list)
        assert len(templates) > 0

    def test_generate_produces_valid_json(self, simple_metadata):
        """Test that generation produces valid JSON-serializable output."""
        import json
        from datetime import datetime

        service = DashboardGenerationService()
        result = service.generate(simple_metadata)

        # Should be serializable
        try:
            json.dumps(result, default=str)
        except TypeError:
            pytest.fail("Generated output is not JSON serializable")


# Performance Tests


class TestPerformance:
    """Performance and stress tests."""

    def test_large_system_generation(self):
        """Test generation with large number of sensors."""
        sensors = []
        for i in range(20):
            signals = []
            for j in range(10):
                signals.append(
                    IndustrialSignalMetadata(
                        id=str(uuid4()),
                        tag=f"SIG_{i}_{j}",
                        name=f"Signal {i}-{j}",
                        data_type="float",
                        direction="input",
                    )
                )
            sensors.append(
                IndustrialSensorMetadata(
                    id=str(uuid4()),
                    code=f"SEN_{i}",
                    name=f"Sensor {i}",
                    sensor_type="test",
                    signals=signals,
                )
            )

        metadata = IndustrialSystemMetadata(
            id=uuid4(),
            name="Large System",
            code="LARGE_SYS",
            sensors=sensors,
        )

        service = DashboardGenerationService()
        result = service.generate(metadata)

        # Should complete and produce components
        assert len(result["components"]) > 0
        assert result["metrics"]["component_count"] > 0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
