# Dashboard Generation Engine - Quick Start

## Installation

The Dashboard Generation Engine is already integrated into the backend. No additional dependencies needed beyond what's already in `requirements.txt`.

## Basic Usage

### 1. Quick Generation

```python
from app.services.dashboard_service import generate_dashboard
from app.dashboard.schemas import IndustrialSystemMetadata

# Given an IndustrialSystemMetadata object
metadata = IndustrialSystemMetadata(...)

# Generate dashboard
dashboard_json = generate_dashboard(metadata)

# dashboard_json contains:
# {
#   "layout": {...},
#   "components": [...],
#   "metadata": {...},
#   "generation_context": {...},
#   "metrics": {...}
# }
```

### 2. Using the Service

```python
from app.services.dashboard_service import DashboardGenerationService

service = DashboardGenerationService()

# Get raw recommendations
recommendations = service.get_raw_recommendations(metadata)

# Get matched templates
templates = service.get_matched_templates(metadata)

# Generate full dashboard
dashboard = service.generate(metadata)
```

### 3. Custom Rules

```python
from app.dashboard.schemas import Rule

rules = [
    Rule(
        id="custom_rule_1",
        name="My Custom Rule",
        conditions={
            "signal_count": {"min": 10},
            "sensor_count": {"min": 5},
        },
        actions={
            "theme": "dark",
            "priority_layout": "detailed",
        },
        priority=10,
    ),
]

dashboard = service.generate_with_custom_rules(metadata, rules)
```

## Integration with API

### 1. Create a Router Endpoint

```python
# In routers/dashboards.py
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas import MetadataRead
from app.services.dashboard_service import DashboardGenerationService

router = APIRouter(prefix="/api/dashboards", tags=["dashboards"])


@router.post("/generate/{metadata_id}", response_model=dict)
def generate_dashboard_from_metadata(
    metadata_id: str,
    db: Session = Depends(get_db),
):
    """Generate dashboard from metadata."""
    from app.repositories.metadata_repository import MetadataRepository

    repo = MetadataRepository(db)
    metadata_record = repo.get_metadata(UUID(metadata_id))

    if not metadata_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metadata not found",
        )

    # Convert to dashboard metadata schema
    from app.dashboard.schemas import (
        IndustrialSystemMetadata,
        IndustrialSensorMetadata,
        IndustrialSignalMetadata,
    )

    signals = [
        IndustrialSignalMetadata(
            id=str(sig.id),
            tag=sig.tag,
            name=sig.name,
            data_type=sig.data_type.value,
            direction=sig.direction.value,
            unit=sig.unit,
            min_value=sig.min_value,
            max_value=sig.max_value,
            description=sig.description,
        )
        for sensor in metadata_record.sensors
        for sig in sensor.signals
    ]

    sensors_meta = [
        IndustrialSensorMetadata(
            id=str(sensor.id),
            code=sensor.code,
            name=sensor.name,
            sensor_type=sensor.sensor_type,
            description=sensor.description,
            signals=[
                IndustrialSignalMetadata(
                    id=str(sig.id),
                    tag=sig.tag,
                    name=sig.name,
                    data_type=sig.data_type.value,
                    direction=sig.direction.value,
                    unit=sig.unit,
                    min_value=sig.min_value,
                    max_value=sig.max_value,
                )
                for sig in sensor.signals
            ],
        )
        for sensor in metadata_record.sensors
    ]

    dashboard_metadata = IndustrialSystemMetadata(
        id=metadata_record.id,
        name=metadata_record.name,
        code=metadata_record.code,
        description=metadata_record.description,
        system_type=metadata_record.system_type,
        location=metadata_record.location,
        sensors=sensors_meta,
    )

    # Generate dashboard
    service = DashboardGenerationService()
    dashboard_json = service.generate(dashboard_metadata)

    return dashboard_json
```

### 2. Add to API Router

```python
# In routers/api.py
from app.routers import dashboards

router = APIRouter(prefix="/api/v1")
router.include_router(dashboards.router)
```

### 3. Use in FastAPI App

```python
# In main.py
from app.routers.dashboards import router as dashboard_router

app.include_router(dashboard_router)
```

## Module Structure

```
app/
├── dashboard/                 # Dashboard Generation Engine
│   ├── __init__.py
│   ├── schemas.py            # Pydantic models
│   ├── rules_engine.py       # Rules evaluation
│   ├── template_manager.py   # Template management
│   ├── components.py         # Component recommendations
│   ├── layout_generator.py   # Layout positioning
│   ├── schema_builder.py     # JSON schema output
│   ├── examples.py           # Usage examples
│   ├── test_dashboard.py     # Unit tests
│   └── README.md             # Documentation
└── services/
    └── dashboard_service.py  # Main orchestration service
```

## Key Concepts

### Rules Engine
- Evaluates system characteristics
- Determines dashboard behavior
- Supports complex conditions with priorities

### Template Manager
- Pre-built for common scenarios
- Matches metadata to templates
- Provides consistent layouts

### Component Recommender
- Analyzes signal types
- Suggests visualization components
- Provides confidence scores

### Layout Generator
- Positions components on grid
- Optimizes space usage
- Handles grid expansion

### Schema Builder
- Converts to final JSON format
- Adds metadata and metrics
- Supports theme customization

## Example Output

```json
{
  "layout": {
    "grid_width": 12,
    "grid_height": 20,
    "spacing": 12,
    "theme": "light",
    "system_info": {
      "name": "Manufacturing Line A",
      "sensor_count": 3,
      "signal_count": 8
    }
  },
  "components": [
    {
      "component": {
        "type": "stat_card",
        "title": "Motor Speed (MOTOR_1_SPEED)",
        "bindings": [
          {
            "source_type": "signal",
            "source_id": "...",
            "source_tag": "MOTOR_1_SPEED",
            "property_name": "value"
          }
        ],
        "properties": {
          "unit": "RPM",
          "precision": 2,
          "show_trend": true
        },
        "refresh_interval": 5
      },
      "position": {
        "row": 0,
        "col": 0,
        "width": 3,
        "height": 3
      }
    }
  ],
  "metadata": {
    "created_at": "2024-01-15T10:30:00",
    "version": "1.0",
    "component_count": 8
  },
  "generation_context": {
    "rules_applied": 1,
    "template_matched": "multi_sensor",
    "recommendations_count": 8,
    "layout_reasoning": "Added 3 stat cards for key metrics..."
  },
  "metrics": {
    "total_cells": 240,
    "used_cells": 156,
    "utilization": 65.0,
    "grid_efficiency": "good"
  }
}
```

## Advanced Usage

### Get Intermediate Results

```python
service = DashboardGenerationService()

# Raw recommendations
recommendations = service.get_raw_recommendations(metadata)
print(f"Confidence: {recommendations.recommendations[0].confidence}")

# Matched templates
templates = service.get_matched_templates(metadata)
print(f"Template: {templates[0]}")

# Generated layout before schema
components = service.get_generated_layout(metadata)
print(f"Component count: {len(components)}")

# Full generation
dashboard = service.generate(metadata)
print(f"Utilization: {dashboard['metrics']['utilization']}%")
```

### Custom Theme

```python
from app.dashboard.schema_builder import JsonSchemaBuilder

builder = JsonSchemaBuilder()
dashboard_json = builder.build_json(components)

# Add custom theme
dashboard_json = builder.add_theme(
    dashboard_json,
    theme_name="dark",
    custom_theme={
        "primary": "#FF5722",
        "secondary": "#2196F3",
    }
)
```

### Add Interactions

```python
dashboard_json = builder.add_interactions(
    dashboard_json,
    interactions=[
        {
            "event": "component_click",
            "actions": ["drill_down", "export"],
        },
    ]
)
```

## Testing

Run tests:
```bash
pytest app/dashboard/test_dashboard.py -v
```

Run examples:
```bash
python -m app.dashboard.examples
```

## Performance

- Simple metadata (1-5 sensors): ~10ms
- Complex metadata (20+ sensors): ~50ms
- Large system (50+ sensors): ~100ms

Optimizations:
- Grid caching
- Early template filtering
- Sorted processing
- Lazy grid expansion

## Troubleshooting

### No components generated
- Check metadata has at least one signal
- Verify signal data types are recognized
- Check rules don't filter all components

### Components overlap
- Layout generator should prevent this
- If it occurs, try enabling optimization
- Check grid size is sufficient

### Poor grid utilization
- Consider custom component sizes
- Adjust grid dimensions
- Use layout optimization

## Next Steps

1. Integrate with metadata service
2. Create API endpoint
3. Add to dashboard UI
4. Test with real industrial data
5. Customize templates for your systems
6. Add custom rules for business logic
