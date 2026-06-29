# Schema-Driven Rendering System

Complete JSON-to-React dashboard rendering engine with component registry, dynamic loading, and schema transformation.

## Overview

The Schema-Driven Rendering System enables you to define industrial dashboards in JSON and automatically convert them to interactive React components. No manual component wiring required.

### Key Features

✅ **Component Registry** - Centralized mapping of component types to React components
✅ **Dynamic Rendering** - Convert JSON schemas to React component trees
✅ **5 Pre-built Widgets** - Temperature/Pressure gauges, trend charts, alarm banners, metric cards
✅ **Dynamic Loading** - Lazy loading and component caching for performance
✅ **Schema Validation** - Validate schemas before rendering
✅ **Data Transformation** - Map raw data to component props
✅ **Error Handling** - Graceful error recovery with fallback components
✅ **Layout System** - Grid, flex, and stack layouts
✅ **Extensible** - Register custom components at runtime

## Architecture

```
Schema JSON
    ↓
Validation → Registry Lookup → Engine Rendering
    ↓            ↓
  Errors    Components
    ↓            ↓
Loader → Dynamic Loading → React Components
    ↓
Cache Management
```

## System Components

### 1. Component Registry (`registry.js`)

Maps component type strings to React components with metadata.

```javascript
import {
  getComponent,
  getComponentByType,
  isComponentRegistered,
  registerComponent,
  getComponentMetadata,
} from '@/schema-renderer'

// Get component
const TemperatureGauge = getComponentByType('temperature_gauge')

// Register custom component
registerComponent('my_widget', MyWidget, {
  displayName: 'My Widget',
  category: 'custom',
  description: 'Custom widget for data visualization',
  defaultProps: { showLegend: true },
})
```

### 2. Rendering Engine (`engine.js`)

Transforms JSON schemas into React component trees.

```javascript
import { renderDashboard, renderComponent, transformData } from '@/schema-renderer'

// Render complete dashboard
const dashboard = renderDashboard(schema, {
  onError: (error) => console.error(error),
  onComponentRender: (schema) => console.log('Rendered', schema),
})

// Transform data for components
const props = transformData(rawData, {
  mapping: {
    temperature: 'sensor.temperature.current',
    pressure: 'sensor.pressure.current',
  },
})
```

### 3. Dynamic Loader (`loader.js`)

Manages component lifecycle, caching, and dynamic registration.

```javascript
import {
  loadComponent,
  preloadComponents,
  registerCustomComponent,
  useComponentLoader,
} from '@/schema-renderer'

// Load component
const Component = loadComponent('temperature_gauge', { lazy: true })

// Preload critical components
await preloadComponents(['temperature_gauge', 'pressure_gauge'])

// Register at runtime
registerCustomComponent('my_widget', CustomWidget)
```

### 4. Pre-built Widgets

#### TemperatureGauge

Circular gauge for temperature with animated needle and thresholds.

```jsx
<TemperatureGauge
  value={75}
  min={0}
  max={100}
  unit="°C"
  warning={80}
  critical={90}
  showScale={true}
  showValue={true}
  onThresholdExceeded={(e) => console.log(e)}
/>
```

#### PressureGauge

Circular gauge for pressure with zone colors and scale.

```jsx
<PressureGauge
  value={5.5}
  min={0}
  max={10}
  unit="bar"
  warning={8}
  critical={9.5}
  showScale={true}
/>
```

#### TrendChart

Time-series line chart for trending data with multiple series.

```jsx
<TrendChart
  title="Temperature Trend"
  data={[
    { timestamp: 0, temp: 20, humidity: 45 },
    { timestamp: 1, temp: 22, humidity: 48 },
    { timestamp: 2, temp: 25, humidity: 50 },
  ]}
  series={[
    { key: 'temp', label: 'Temperature (°C)', color: '#ef4444' },
    { key: 'humidity', label: 'Humidity (%)', color: '#3b82f6' },
  ]}
  timeRange="1h"
  showLegend={true}
  height={300}
/>
```

#### AlarmBanner

Display active alarms with severity levels and actions.

```jsx
<AlarmBanner
  alarms={[
    {
      id: 'alarm-1',
      title: 'High Temperature',
      message: 'Sensor T-01 exceeded warning threshold',
      severity: 'warning',
      source: 'T-01',
      timestamp: new Date(),
    },
  ]}
  showBorder={true}
  sound={false}
  maxAlarms={5}
  onAlarmClick={(alarm) => console.log(alarm)}
/>
```

#### MetricCard

Single metric display with status indicator and trend.

```jsx
<MetricCard
  title="Temperature"
  value={75.5}
  unit="°C"
  status="normal"
  trend={{ value: 2.5, percentage: 3.5, direction: 'up' }}
  warningThreshold={80}
  criticalThreshold={90}
  showTrend={true}
/>
```

## Schema Format

### Complete Dashboard Schema

```json
{
  "version": "1.0",
  "title": "Industrial Dashboard",
  "description": "Real-time monitoring dashboard",
  "layout": {
    "type": "grid",
    "columns": 3,
    "gap": 4,
    "components": [
      {
        "id": "temp-gauge-1",
        "type": "temperature_gauge",
        "props": {
          "title": "Reactor Temperature",
          "value": 75,
          "min": 0,
          "max": 100,
          "unit": "°C",
          "warning": 80,
          "critical": 90
        }
      },
      {
        "id": "pressure-gauge-1",
        "type": "pressure_gauge",
        "props": {
          "title": "System Pressure",
          "value": 5.5,
          "min": 0,
          "max": 10,
          "unit": "bar"
        }
      },
      {
        "id": "trend-chart-1",
        "type": "trend_chart",
        "props": {
          "title": "24-Hour Trend",
          "timeRange": "24h",
          "showLegend": true,
          "colors": ["#ef4444", "#3b82f6"]
        }
      }
    ]
  }
}
```

### Layout Types

#### Grid Layout

```json
{
  "type": "grid",
  "columns": 3,
  "gap": 4,
  "components": [...]
}
```

#### Flex Layout

```json
{
  "type": "flex",
  "direction": "row",
  "wrap": true,
  "justify": "start",
  "align": "stretch",
  "components": [...]
}
```

#### Stack Layout

```json
{
  "type": "stack",
  "components": [...]
}
```

## Component Schema

Each component in schema must include:

```json
{
  "id": "unique-identifier",
  "type": "temperature_gauge",
  "props": {
    "value": 75,
    "min": 0,
    "max": 100
  }
}
```

### Supported Types

- `temperature_gauge` - Circular temperature gauge
- `pressure_gauge` - Circular pressure gauge
- `trend_chart` - Time-series line chart
- `alarm_banner` - Active alarms display
- `metric_card` - Single metric with status

## Data Transformation

Map raw data to component props:

```javascript
const schema = {
  components: [{
    type: 'temperature_gauge',
    props: { value: 0 } // Will be filled by transformation
  }]
}

const data = {
  sensor: {
    temperature: {
      current: 75
    }
  }
}

const transformConfig = {
  mapping: {
    value: 'sensor.temperature.current'
  }
}

const props = transformData(data, transformConfig)
// props = { value: 75 }
```

### Transformation Types

**Simple path mapping:**
```javascript
mapping: {
  temperature: 'sensor.temperature.current'
}
```

**Custom transform function:**
```javascript
mapping: {
  temperature: (data) => data.sensor.readings[0].temp
}
```

**Complex mapping:**
```javascript
mapping: {
  temperature: {
    path: 'sensor.temperature.current',
    default: 0
  }
}
```

## Usage in React

### Basic Usage

```jsx
import SchemaRenderer from '@/schema-renderer'

export function DashboardPage() {
  const schema = {
    title: 'My Dashboard',
    components: [...]
  }

  return <SchemaRenderer schema={schema} />
}
```

### With Data

```jsx
export function DashboardPage() {
  const [sensorData, setSensorData] = useState(null)

  useEffect(() => {
    // Fetch sensor data
    fetchSensorData().then(setSensorData)
  }, [])

  const schema = { /* schema */ }

  return (
    <SchemaRenderer
      schema={schema}
      data={sensorData}
      onError={(error) => console.error(error)}
    />
  )
}
```

### With Async Data

```jsx
import { useSchemaRenderer } from '@/schema-renderer'

export function DashboardPage() {
  const schema = { /* schema */ }

  const { data, loading, error, refetch } = useSchemaRenderer(
    schema,
    async () => {
      const response = await fetch('/api/sensor-data')
      return response.json()
    }
  )

  return (
    <SchemaRenderer
      schema={schema}
      data={data}
      loading={loading}
      error={error}
      refetch={refetch}
    />
  )
}
```

## Registry API

### Core Functions

```javascript
// Get component metadata
const metadata = getComponentMetadata('temperature_gauge')
// { displayName: 'Temperature Gauge', category: 'gauge', ... }

// Get components by category
const gauges = getComponentsByCategory('gauge')

// Validate schema
const { valid, errors } = validateComponentSchema({
  type: 'unknown_type'
})

// Get default props
const defaults = getDefaultProps('temperature_gauge')

// Get available types
const types = getAvailableTypes()
// ['temperature_gauge', 'pressure_gauge', 'trend_chart', 'alarm_banner', 'metric_card']
```

## Loader API

### Component Caching

```javascript
// Preload components
await preloadComponents(['temperature_gauge', 'pressure_gauge'])

// Check cache stats
const stats = getCacheStats()
// { cached: 2, custom: 0, total: 2 }

// Clear cache
clearComponentCache()
// or specific type
clearComponentCache('temperature_gauge')
```

### Custom Components

```javascript
// Register custom component
registerCustomComponent('my_gauge', MyGaugeComponent, {
  override: false
})

// Get loadable components
const loadable = getLoadableComponents()

// Get component info
const info = getComponentInfo('temperature_gauge')
```

## Engine API

### Rendering Functions

```javascript
// Render single component
renderComponent({ type: 'temperature_gauge', props: {...} })

// Render multiple components
renderComponents([...schemas])

// Render layout
renderLayout({ type: 'grid', columns: 3, components: [...] })

// Render complete dashboard
renderDashboard(schema)
```

### Data Utilities

```javascript
// Get nested data by path
const temp = getDataByPath(data, 'sensor.temperature.current', 0)

// Merge schemas (composition)
const merged = mergeSchemas(baseSchema, overaysSchema)
```

## Error Handling

Custom error components are rendered automatically:

```jsx
// Missing component type
<div className="p-4 bg-yellow-50">
  <p>Missing Component</p>
  <p>Type: unknown_type</p>
</div>

// Rendering error
<div className="p-4 bg-red-50">
  <p>Rendering Error</p>
  <p>{error.message}</p>
</div>
```

### Error Callbacks

```jsx
<SchemaRenderer
  schema={schema}
  onError={(error) => {
    console.error('Render error:', error)
    trackError(error)
  }}
  onComponentRender={(schema) => {
    console.log('Rendered:', schema.id)
  }}
/>
```

## Performance Optimization

### Lazy Loading

```javascript
// Enable lazy loading for non-critical components
const Component = loadComponent('trend_chart', { lazy: true })
```

### Code Splitting

```javascript
// Preload critical path components
await preloadComponents(['temperature_gauge', 'alarm_banner'])
```

### Caching

```javascript
// Components are cached by default
// Clear cache for hot reloading
clearComponentCache()
```

## Examples

### Real-time Monitor Dashboard

```json
{
  "version": "1.0",
  "title": "Real-time Monitor",
  "layout": {
    "type": "grid",
    "columns": 2,
    "gap": 4,
    "components": [
      {
        "id": "alarms",
        "type": "alarm_banner",
        "props": { "maxAlarms": 10 }
      },
      {
        "id": "temp",
        "type": "temperature_gauge",
        "props": { "title": "Reactor Temp", "value": 75 }
      },
      {
        "id": "pressure",
        "type": "pressure_gauge",
        "props": { "title": "System Pressure", "value": 5.5 }
      },
      {
        "id": "trend",
        "type": "trend_chart",
        "props": { "title": "24h Trend", "timeRange": "24h" }
      }
    ]
  }
}
```

### Metrics Dashboard

```jsx
export function MetricsDashboard() {
  const [metrics, setMetrics] = useState([])

  const schema = {
    title: 'System Metrics',
    layout: {
      type: 'grid',
      columns: 4,
      components: metrics.map(m => ({
        type: 'metric_card',
        props: {
          title: m.name,
          value: m.current,
          unit: m.unit,
          status: m.status,
          trend: m.trend,
        }
      }))
    }
  }

  return <SchemaRenderer schema={schema} />
}
```

## Best Practices

1. **Validate schemas** - Always validate before rendering
2. **Use component IDs** - For tracking and debugging
3. **Preload critical components** - Improve perceived performance
4. **Transform data early** - Map data before rendering
5. **Handle errors gracefully** - Provide fallback UI
6. **Cache appropriately** - Use registry caching for performance
7. **Register custom components** - Extend registry for custom widgets
8. **Document schemas** - Include comments for maintainability

## Migration Guide

### From Manual Components to Schema-Driven

**Before:**
```jsx
<div className="grid grid-cols-3 gap-4">
  <TemperatureGauge value={75} min={0} max={100} />
  <PressureGauge value={5.5} min={0} max={10} />
  <TrendChart data={trendData} />
</div>
```

**After:**
```jsx
const schema = {
  layout: { type: 'grid', columns: 3, gap: 4, components: [...] }
}
<SchemaRenderer schema={schema} data={sensorData} />
```

## Troubleshooting

### Schema Validation Failed

Check your schema structure:
```javascript
const { valid, errors } = validateComponentSchema(schema)
console.error(errors) // Get specific validation errors
```

### Component Not Found

Verify component is registered:
```javascript
const available = getAvailableTypes()
console.log('Available:', available)
```

### Data Not Showing

Check data transformation:
```javascript
const props = transformData(rawData, transformConfig)
console.log('Transformed:', props)
```

### Performance Issues

Profile rendering and preload components:
```javascript
await preloadComponents(['temperature_gauge', 'pressure_gauge'])
// Verify cache
const stats = getCacheStats()
```

---

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Components**: 5 built-in + extensible with custom
