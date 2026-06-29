# Dashboard Generation Engine

## Overview

The Dashboard Generation Engine transforms industrial metadata into optimized dashboard layouts in JSON format. It combines:

- **Rules Engine**: Evaluates system characteristics to determine behavior
- **Template Manager**: Retrieves and applies pre-built dashboard templates
- **Component Recommender**: Suggests appropriate visualization components
- **Layout Generator**: Positions components on a grid with optimization
- **Schema Builder**: Outputs final JSON layout schema

## Architecture

```
Industrial Metadata
        ↓
    [Rules Engine]
        ↓
  [Template Manager]
        ↓
[Recommendation Engine]
        ↓
  [Layout Generator]
        ↓
  [Schema Builder]
        ↓
    JSON Layout Schema
```

## Core Components

### 1. Rules Engine (`rules_engine.py`)

Evaluates system metadata against defined rules to influence dashboard generation.

**Features:**
- Condition-based rule matching
- Priority-based execution
- Support for numeric ranges, boolean checks, and collections

**Condition Types:**
- `signal_count`: Number of signals (range: `{"min": 5, "max": 50}`)
- `sensor_count`: Number of sensors
- `has_alarms`: Boolean flag for alarm presence
- `system_type`: System classification
- `signal_types`: Set of data types present

**Example:**
```python
rule = Rule(
    id="high_volume",
    name="High Volume System",
    conditions={
        "signal_count": {"min": 20},
        "sensor_count": {"min": 5},
    },
    actions={"layout_type": "comprehensive"},
    priority=10,
)
```

### 2. Template Manager (`template_manager.py`)

Manages dashboard templates for different system types.

**Built-in Templates:**
- `simple_monitoring`: 1-3 sensors, 1-10 signals
- `multi_sensor`: 4-20 sensors, 10-50 signals
- `alarm_monitoring`: Systems with alarms
- `complex_industrial`: 20+ sensors, 50+ signals

**Template Structure:**
```python
template = TemplateDefinition(
    id="template_id",
    name="Template Name",
    applies_to={"sensor_count": {"min": 5}},
    layout_config={"grid_width": 12, "theme": "light"},
    component_templates=[...],
    priority=10,
)
```

### 3. Component Recommendation Engine (`components.py`)

Analyzes metadata and recommends visualization components.

**Supported Components:**
- `stat_card`: Key metrics display
- `gauge`: Analog value visualization
- `line_chart`: Time series trends
- `bar_chart`: Comparative analysis
- `table`: Detailed data view
- `alarm_panel`: Alarm status/history
- `indicator`: Binary status
- `trend`: Quick trend visualization
- `heatmap`: 2D data matrix

**Recommendation Algorithm:**
1. Categorizes signals by data type
2. Assigns components based on signal characteristics
3. Prioritizes high-confidence recommendations
4. Suggests component properties and bindings

**Example Output:**
```python
ComponentRecommendation(
    component_type=ComponentType.GAUGE,
    reasoning="Analog gauge for pressure with range 0-100 bar",
    confidence=0.85,
    source_bindings=[...],
    suggested_properties={"min": 0, "max": 100},
)
```

### 4. Layout Generator (`layout_generator.py`)

Positions components on a dashboard grid.

**Features:**
- Grid-based positioning (12x20 by default)
- Component-specific sizing rules
- Automatic space optimization
- Layout metrics calculation

**Component Sizing:**
- Stat Card: 3x3
- Gauge: 3x4
- Line Chart: 6x4
- Alarm Panel: 12x5
- Table: 12x6

**Grid Placement Algorithm:**
- Sorts components by confidence
- Finds first available position (top-left priority)
- Expands grid if needed
- Optimizes for minimal wasted space

### 5. JSON Schema Builder (`schema_builder.py`)

Converts components into final JSON schema.

**Output Format:**
```json
{
  "layout": {
    "grid_width": 12,
    "grid_height": 20,
    "spacing": 12,
    "theme": "light",
    "system_info": {...}
  },
  "components": [
    {
      "component": {
        "type": "gauge",
        "title": "Motor Speed",
        "bindings": [...],
        "properties": {...},
        "refresh_interval": 5
      },
      "position": {
        "row": 0,
        "col": 0,
        "width": 3,
        "height": 4
      }
    }
  ],
  "metadata": {
    "created_at": "2024-01-15T10:30:00",
    "version": "1.0",
    "component_count": 8
  }
}
```

## Usage

### Basic Generation

```python
from app.services.dashboard_service import generate_dashboard
from app.dashboard.schemas import IndustrialSystemMetadata

# Create or load metadata
metadata = IndustrialSystemMetadata(...)

# Generate dashboard
dashboard_json = generate_dashboard(metadata)
```

### Advanced Generation with Service

```python
from app.services.dashboard_service import DashboardGenerationService

service = DashboardGenerationService()

# Get recommendations
recommendations = service.get_raw_recommendations(metadata)

# Get matched templates
templates = service.get_matched_templates(metadata)

# Generate with full context
dashboard = service.generate(metadata)
```

### Custom Rules

```python
from app.dashboard.schemas import Rule

custom_rules = [
    Rule(
        id="custom_1",
        name="Custom Rule",
        conditions={"sensor_count": {"min": 5}},
        actions={"theme": "dark"},
        priority=10,
    ),
]

dashboard = service.generate_with_custom_rules(metadata, custom_rules)
```

### Layout Inspection

```python
# Get components before schema building
components = service.get_generated_layout(metadata)

# Calculate metrics
metrics = service.layout_generator.calculate_layout_metrics(components)
print(f"Utilization: {metrics['utilization']}%")
print(f"Grid Efficiency: {metrics['grid_efficiency']}")
```

## Data Flow

### Input (Industrial Metadata)
```python
IndustrialSystemMetadata
├── system info (name, code, type, location)
├── sensors[]
│   └── sensor info (code, name, type)
│       └── signals[]
│           └── signal (tag, name, data_type, unit, range)
└── alarms[]
```

### Output (JSON Layout Schema)
```python
LayoutSchema
├── layout (metadata)
├── components[]
│   ├── component config (type, title, bindings, properties)
│   └── position (row, col, width, height)
└── metadata (created_at, version, count)
```

## Algorithms

### Rule Matching
1. Build context from metadata
2. Evaluate each rule's conditions
3. Sort matched rules by priority
4. Return results with action payloads

### Template Selection
1. Extract system characteristics
2. Compare against template criteria
3. Sort by priority
4. Return best matches

### Component Recommendation
1. Categorize signals by data type
2. Assign components based on characteristics:
   - Numeric signals → Gauges, Stat Cards, Trend
   - Boolean signals → Indicators
   - Multiple signals → Line Charts, Tables
   - Alarms present → Alarm Panel
3. Generate confidence scores
4. Sort by confidence

### Layout Positioning
1. Create empty grid
2. For each component (sorted by confidence):
   - Find first available position
   - If no space, expand grid
   - Mark cells as occupied
3. Calculate metrics
4. Optimize if needed

## Configuration

### Grid Configuration
```python
layout_generator = LayoutGenerator(grid_width=12, grid_height=20)
```

### Component Sizing
Customize in `LayoutGenerator.COMPONENT_SIZES`:
```python
COMPONENT_SIZES = {
    ComponentType.GAUGE: {"width": 3, "height": 4},
    # ... more types
}
```

### Themes
Available themes: `light`, `dark`
Custom theme support in schema builder:
```python
schema_builder.add_theme(json_output, custom_theme={...})
```

## Extensibility

### Add Custom Rules
```python
engine = RulesEngine()
engine.add_rule(custom_rule)
matches = engine.evaluate(context)
```

### Add Custom Templates
```python
manager = TemplateManager()
manager.register_template(custom_template)
```

### Create Custom Components
Add to `ComponentType` enum and update `COMPONENT_SIZES`.

## Performance Considerations

### Optimization Strategies
1. **Early Filtering**: Templates reduce recommendation set early
2. **Grid Caching**: Marks occupied cells to avoid re-checking
3. **Sorting**: Prioritizes high-confidence recommendations
4. **Lazy Expansion**: Grid expands only when needed

### Metrics
- `utilization`: Percentage of grid cells used
- `grid_efficiency`: Qualitative assessment (good/fair/poor)
- `component_count`: Total components placed
- `time_to_generate`: Generation time (when profiled)

## Testing

See `examples.py` for comprehensive usage examples:
- Basic generation
- Service customization
- Custom rules
- Layout inspection
- Large systems
- Schema output

## Error Handling

The engine gracefully handles:
- Missing sensors/signals (empty recommendations)
- Invalid template criteria
- Grid overflow (automatic expansion)
- Missing component sizes (defaults to 4x4)

## Future Enhancements

- [ ] ML-based component recommendation
- [ ] A/B testing framework
- [ ] User preference learning
- [ ] Real-time layout adjustment
- [ ] Advanced animations
- [ ] Mobile-responsive layouts
- [ ] Dark mode optimization
- [ ] Accessibility improvements
