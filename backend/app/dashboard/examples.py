"""
Example usage of the Dashboard Generation Engine.

Demonstrates:
- Creating industrial metadata
- Generating dashboards
- Using rules and templates
- Customizing generation
"""

import json
from uuid import uuid4

from app.dashboard.schemas import (
    IndustrialSensorMetadata,
    IndustrialSignalMetadata,
    IndustrialSystemMetadata,
    Rule,
)
from app.services.dashboard_service import DashboardGenerationService, generate_dashboard


# Example 1: Create sample industrial metadata
def create_sample_manufacturing_system() -> IndustrialSystemMetadata:
    """Create sample manufacturing system metadata."""
    signals_motor_1 = [
        IndustrialSignalMetadata(
            id=str(uuid4()),
            tag="MOTOR_1_SPEED",
            name="Motor 1 Speed",
            data_type="float",
            direction="input",
            unit="RPM",
            min_value=0,
            max_value=5000,
            description="Main motor spindle speed",
        ),
        IndustrialSignalMetadata(
            id=str(uuid4()),
            tag="MOTOR_1_CURRENT",
            name="Motor 1 Current",
            data_type="float",
            direction="input",
            unit="A",
            min_value=0,
            max_value=50,
            description="Motor current draw",
        ),
        IndustrialSignalMetadata(
            id=str(uuid4()),
            tag="MOTOR_1_TEMP",
            name="Motor 1 Temperature",
            data_type="float",
            direction="input",
            unit="°C",
            min_value=0,
            max_value=100,
            description="Motor winding temperature",
        ),
    ]

    sensor_motor_1 = IndustrialSensorMetadata(
        id=str(uuid4()),
        code="MTR_001",
        name="Main Motor",
        sensor_type="three_phase_motor",
        description="Primary production motor",
        signals=signals_motor_1,
    )

    signals_conveyor = [
        IndustrialSignalMetadata(
            id=str(uuid4()),
            tag="CONV_SPEED",
            name="Conveyor Speed",
            data_type="float",
            direction="input",
            unit="m/s",
            min_value=0,
            max_value=2,
        ),
        IndustrialSignalMetadata(
            id=str(uuid4()),
            tag="CONV_RUNNING",
            name="Conveyor Running",
            data_type="boolean",
            direction="input",
        ),
    ]

    sensor_conveyor = IndustrialSensorMetadata(
        id=str(uuid4()),
        code="CNV_001",
        name="Main Conveyor",
        sensor_type="conveyor",
        signals=signals_conveyor,
    )

    signals_press = [
        IndustrialSignalMetadata(
            id=str(uuid4()),
            tag="PRESS_FORCE",
            name="Press Force",
            data_type="float",
            direction="input",
            unit="kN",
            min_value=0,
            max_value=500,
        ),
        IndustrialSignalMetadata(
            id=str(uuid4()),
            tag="PRESS_CYCLES",
            name="Cycle Count",
            data_type="int",
            direction="input",
        ),
    ]

    sensor_press = IndustrialSensorMetadata(
        id=str(uuid4()),
        code="PRS_001",
        name="Hydraulic Press",
        sensor_type="press",
        signals=signals_press,
    )

    return IndustrialSystemMetadata(
        id=uuid4(),
        name="Manufacturing Line A",
        code="MFG_LINE_A",
        description="Primary manufacturing production line",
        system_type="manufacturing",
        location="Building 1, Floor 2",
        sensors=[sensor_motor_1, sensor_conveyor, sensor_press],
        alarms=[
            {"id": "ALM_001", "name": "Motor Over Temperature"},
            {"id": "ALM_002", "name": "Conveyor Stopped"},
            {"id": "ALM_003", "name": "Press Overpressure"},
        ],
    )


# Example 2: Basic generation
def example_basic_generation():
    """Example: Basic dashboard generation."""
    print("\n=== Example 1: Basic Generation ===")

    metadata = create_sample_manufacturing_system()
    dashboard = generate_dashboard(metadata)

    print(f"Generated dashboard with {len(dashboard.get('components', []))} components")
    print(f"Layout reasoning: {dashboard.get('generation_context', {}).get('layout_reasoning')}")
    print(f"Metrics: {dashboard.get('metrics', {})}")

    return dashboard


# Example 3: Service with customization
def example_service_customization():
    """Example: Using service with customization."""
    print("\n=== Example 2: Service Customization ===")

    service = DashboardGenerationService()
    metadata = create_sample_manufacturing_system()

    # Get raw recommendations first
    recommendations = service.get_raw_recommendations(metadata)
    print(f"Generated {len(recommendations.recommendations)} recommendations")
    for rec in recommendations.recommendations[:3]:
        print(f"  - {rec.component_type.value}: {rec.reasoning}")

    # Get matched templates
    templates = service.get_matched_templates(metadata)
    print(f"Matched templates: {templates}")

    # Full generation
    dashboard = service.generate(metadata)
    return dashboard


# Example 4: Custom rules
def example_custom_rules():
    """Example: Generation with custom rules."""
    print("\n=== Example 3: Custom Rules ===")

    service = DashboardGenerationService()
    metadata = create_sample_manufacturing_system()

    # Define custom rules
    custom_rules = [
        Rule(
            id="rule_1",
            name="Motor Heavy Load",
            description="Apply when motor has high signal count",
            conditions={
                "signal_count": {"min": 3},
                "sensor_count": {"min": 1},
            },
            actions={
                "theme": "dark",
                "priority_layout": "motor_focused",
                "update_frequency": 2,
            },
            priority=10,
        ),
        Rule(
            id="rule_2",
            name="Multi-Sensor System",
            description="Multi-sensor production system",
            conditions={
                "sensor_count": {"min": 2},
            },
            actions={
                "layout_type": "comprehensive",
                "enable_comparative_widgets": True,
            },
            priority=5,
        ),
    ]

    dashboard = service.generate_with_custom_rules(metadata, custom_rules)
    print(f"Applied {dashboard.get('generation_context', {}).get('rules_applied')} rules")

    return dashboard


# Example 5: Layout structure inspection
def example_layout_inspection():
    """Example: Inspecting generated layout structure."""
    print("\n=== Example 4: Layout Inspection ===")

    service = DashboardGenerationService()
    metadata = create_sample_manufacturing_system()

    # Get layout before schema building
    components = service.get_generated_layout(metadata)
    print(f"Total components: {len(components)}")

    # Show first few components
    for i, comp in enumerate(components[:3]):
        print(f"\nComponent {i + 1}:")
        print(f"  Type: {comp.component.type.value}")
        print(f"  Title: {comp.component.title}")
        print(f"  Position: Row {comp.position.row}, Col {comp.position.col} "
              f"({comp.position.width}x{comp.position.height})")

    # Get metrics
    metrics = service.layout_generator.calculate_layout_metrics(components)
    print(f"\nLayout Metrics:")
    print(f"  Utilization: {metrics['utilization']}%")
    print(f"  Grid Efficiency: {metrics['grid_efficiency']}")

    return components


# Example 6: Large industrial system
def create_large_manufacturing_system() -> IndustrialSystemMetadata:
    """Create larger industrial system."""
    sensors = []

    for sensor_num in range(1, 11):  # 10 sensors
        signals = []
        for signal_num in range(1, 6):  # 5 signals per sensor
            signals.append(
                IndustrialSignalMetadata(
                    id=str(uuid4()),
                    tag=f"SENSOR_{sensor_num:02d}_SIG_{signal_num:02d}",
                    name=f"Sensor {sensor_num} Signal {signal_num}",
                    data_type="float" if signal_num <= 3 else "boolean",
                    direction="input",
                    unit="unit" if signal_num <= 3 else None,
                    min_value=0 if signal_num <= 3 else None,
                    max_value=100 if signal_num <= 3 else None,
                )
            )

        sensors.append(
            IndustrialSensorMetadata(
                id=str(uuid4()),
                code=f"SEN_{sensor_num:02d}",
                name=f"Industrial Sensor {sensor_num}",
                sensor_type="multi_parameter_sensor",
                signals=signals,
            )
        )

    return IndustrialSystemMetadata(
        id=uuid4(),
        name="Large Industrial Complex",
        code="INDUSTRIAL_COMPLEX_001",
        description="Large multi-sensor industrial system",
        system_type="industrial_complex",
        location="Main facility",
        sensors=sensors,
        alarms=[{"id": f"ALM_{i:03d}", "name": f"Alarm {i}"} for i in range(1, 11)],
    )


def example_large_system():
    """Example: Large industrial system."""
    print("\n=== Example 5: Large Industrial System ===")

    service = DashboardGenerationService()
    metadata = create_large_manufacturing_system()

    dashboard = service.generate(metadata)
    print(f"Generated dashboard with {len(dashboard.get('components', []))} components")
    print(f"Grid height: {dashboard.get('layout', {}).get('grid_height')}")
    print(f"Performance: {dashboard.get('metrics', {})}")

    return dashboard


# Example 7: Pretty print output
def example_pretty_output():
    """Example: Pretty print generated dashboard."""
    print("\n=== Example 6: Schema Output ===")

    metadata = create_sample_manufacturing_system()
    dashboard = generate_dashboard(metadata)

    print(json.dumps(dashboard, indent=2, default=str)[:1000] + "...")


def run_all_examples():
    """Run all examples."""
    example_basic_generation()
    example_service_customization()
    example_custom_rules()
    example_layout_inspection()
    example_large_system()
    example_pretty_output()

    print("\n=== All Examples Completed ===")


if __name__ == "__main__":
    run_all_examples()
