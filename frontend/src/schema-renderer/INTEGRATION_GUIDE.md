# Schema-Driven Rendering + Dashboard Engine Integration

Complete guide for using the Schema-Driven Rendering System with the Backend Dashboard Generation Engine.

## System Architecture

```
┌─────────────────────────────────────┐
│     Industrial Metadata              │
│  (systems, sensors, measurements)   │
└────────────────────┬────────────────┘
                     │
          Backend Dashboard Engine
          (Python FastAPI)
                     │
          ┌──────────▼──────────┐
          │ Rules Engine        │
          │ Template Matcher    │
          │ Component Suggester │
          │ Layout Generator    │
          │ Schema Builder      │
          └──────────┬──────────┘
                     │
          {JSON Dashboard Schema}
                     │
                     ▼
          ┌─────────────────────┐
          │  REST API Response  │
          │  /api/dashboard/    │
          │  generate           │
          └──────────┬──────────┘
                     │
                     ▼
        Frontend React Application
        (Schema-Driven Renderer)
                     │
          ┌──────────▼──────────┐
          │ Schema Validation   │
          │ Component Registry  │
          │ Dynamic Rendering   │
          └──────────┬──────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │ Interactive Dashboard   │
        │ (React Components)      │
        │ Temperature Gauge       │
        │ Pressure Gauge          │
        │ Trend Charts            │
        │ Alarm Banners           │
        │ Metric Cards            │
        └─────────────────────────┘
```

## Backend: Generating Schema

The backend Dashboard Generation Engine creates schemas like this:

```python
from app.services.dashboard_service import DashboardService

service = DashboardService()

# Generate schema from industrial metadata
result = service.generate_dashboard(
    metadata={
        'system_name': 'Reactor System',
        'signal_count': 15,
        'sensor_count': 8,
        'has_alarms': True,
        'system_type': 'process_control',
        'signal_types': {
            'temperature': ['T-01', 'T-02'],
            'pressure': ['P-01', 'P-02'],
            'flow': ['F-01'],
        }
    }
)

# Returns schema dict
schema = result['layout']  # JSON schema ready for React
```

### Backend Schema Output Format

```json
{
  "layout": {
    "type": "grid",
    "columns": 3,
    "gap": 4,
    "components": [
      {
        "type": "temperature_gauge",
        "id": "temp-01",
        "props": {
          "title": "Reactor Temperature",
          "min": 0,
          "max": 100,
          "unit": "°C",
          "warning": 80,
          "critical": 90
        }
      },
      {
        "type": "pressure_gauge",
        "id": "pressure-01",
        "props": {
          "title": "System Pressure",
          "min": 0,
          "max": 10,
          "unit": "bar"
        }
      },
      {
        "type": "trend_chart",
        "id": "trend-01",
        "props": {
          "title": "24-Hour Trend",
          "timeRange": "24h"
        }
      },
      {
        "type": "metric_card",
        "id": "metric-01",
        "props": {
          "title": "System Status",
          "value": 94.5,
          "unit": "%",
          "status": "normal"
        }
      }
    ]
  }
}
```

## Frontend: Consuming API Response

### 1. API Call to Generate Dashboard

```javascript
// src/services/dashboard.js
class DashboardService {
  async generateDashboard(metadataId) {
    const response = await apiClient.post('/dashboard/generate', {
      metadata_id: metadataId
    })
    return response.data
  }

  async getDashboar (id) {
    const response = await apiClient.get(`/dashboard/${id}`)
    return response.data
  }
}

export default new DashboardService()
```

### 2. Component to Display Generated Dashboard

```jsx
// src/pages/DashboardPage.jsx
import { useState, useEffect } from 'react'
import SchemaRenderer from '@/schema-renderer'
import dashboardService from '@/services/dashboard'

export function DashboardPage() {
  const [schema, setSchema] = useState(null)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        // Generate schema from backend
        const result = await dashboardService.generateDashboard(
          'metadata-id-123'
        )
        setSchema(result.layout)

        // Fetch real-time data
        const sensorData = await fetch('/api/sensor-data').then(r => r.json())
        setData(sensorData)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
    // Refresh data every 5 seconds
    const interval = setInterval(loadDashboard, 5000)
    return () => clearInterval(interval)
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <SchemaRenderer
      schema={schema}
      data={data}
      onError={(error) => console.error(error)}
    />
  )
}
```

### 3. With Real-time Data Updates

```jsx
import { useSchemaRenderer } from '@/schema-renderer'

export function RealtimeDashboard() {
  const [metadataId, setMetadataId] = useState('metadata-1')

  const { data, loading, error, refetch } = useSchemaRenderer(
    null, // Will be loaded below
    async () => {
      // Generate schema
      const result = await dashboardService.generateDashboard(metadataId)

      // Fetch sensor data
      const sensorData = await fetch('/api/sensor-data').then(r => r.json())

      return {
        schema: result.layout,
        data: sensorData
      }
    }
  )

  // Load initial schema
  useEffect(() => {
    refetch()
  }, [metadataId, refetch])

  if (loading) return <LoadingSpinner />
  if (error) return <Alert type="error" message={error} />

  return (
    <SchemaRenderer
      schema={data?.schema}
      data={data?.data}
      loading={loading}
      error={error}
    />
  )
}
```

## Complete Integration Example

```jsx
// src/pages/GeneratedDashboardPage.jsx
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import SchemaRenderer from '@/schema-renderer'
import dashboardService from '@/services/dashboard'
import metadataService from '@/services/metadata'
import Alert from '@/components/Alert'
import LoadingSpinner from '@/components/LoadingSpinner'

export function GeneratedDashboardPage() {
  const { metadataId } = useParams()
  const [schema, setSchema] = useState(null)
  const [metadata, setMetadata] = useState(null)
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [refreshInterval, setRefreshInterval] = useState(5000)

  // Load initial data
  useEffect(() => {
    const loadDashboard = async () => {
      try {
        // Get metadata
        const meta = await metadataService.getMetadata(metadataId)
        setMetadata(meta)

        // Generate dashboard schema
        const response = await dashboardService.generateDashboard(metadataId)
        setSchema(response.layout)

        // Load initial sensor data
        const sensorData = await fetch(
          `/api/metadata/${metadataId}/data`
        ).then((r) => r.json())
        setData(sensorData)

        setError(null)
      } catch (err) {
        setError(err.message)
        console.error('Failed to load dashboard:', err)
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [metadataId])

  // Auto-refresh sensor data
  useEffect(() => {
    if (!schema) return

    const interval = setInterval(async () => {
      try {
        const sensorData = await fetch(
          `/api/metadata/${metadataId}/data`
        ).then((r) => r.json())
        setData(sensorData)
      } catch (err) {
        console.error('Failed to refresh data:', err)
      }
    }, refreshInterval)

    return () => clearInterval(interval)
  }, [metadataId, refreshInterval, schema])

  // States
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <Alert
          type="error"
          title="Failed to Load Dashboard"
          message={error}
        />
        <button
          onClick={() => window.location.reload()}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800">{metadata?.name}</h1>
        <p className="text-gray-600 mt-2">{metadata?.description}</p>

        {/* Refresh Control */}
        <div className="mt-4 flex items-center gap-4">
          <label>
            <span className="text-sm font-medium text-gray-700">
              Auto-refresh:
            </span>
            <select
              value={refreshInterval}
              onChange={(e) => setRefreshInterval(Number(e.target.value))}
              className="ml-2 px-3 py-1 border rounded"
            >
              <option value={1000}>1 second</option>
              <option value={5000}>5 seconds</option>
              <option value={10000}>10 seconds</option>
              <option value={30000}>30 seconds</option>
              <option value={60000}>1 minute</option>
            </select>
          </label>

          <button
            onClick={() => window.location.reload()}
            className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
          >
            Refresh Now
          </button>
        </div>
      </div>

      {/* Dashboard Renderer */}
      <SchemaRenderer
        schema={schema}
        data={data}
        onError={(error) => {
          console.error('Rendering error:', error)
          setError(error.message)
        }}
        onComponentRender={(schema) => {
          console.debug(`Rendered component: ${schema.id}`)
        }}
      />

      {/* Debug Info (development only) */}
      {process.env.NODE_ENV === 'development' && (
        <details className="mt-8 p-4 bg-gray-100 rounded text-xs">
          <summary className="cursor-pointer font-bold">Debug Info </summary>
          <pre className="mt-4 overflow-auto">
            {JSON.stringify(
              {
                metadata,
                schema: schema
                  ? { title: schema.type, componentCount: schema.components?.length }
                  : null,
                dataKeys: data ? Object.keys(data) : null,
              },
              null,
              2
            )}
          </pre>
        </details>
      )}
    </div>
  )
}

export default GeneratedDashboardPage
```

## Data Mapping from Backend to Frontend

### Backend generates:
```json
{
  "layout": {
    "components": [
      {
        "type": "temperature_gauge",
        "props": {
          "title": "T-01",
          "min": 0,
          "max": 100
          // value will come from data
        }
      }
    ]
  }
}
```

### Frontend provides live data:
```javascript
const data = {
  'T-01': 75.5,
  'P-01': 5.2,
  'F-01': 120.0
}
```

### Schema Renderer combines them:
```javascript
<TemperatureGauge
  title="T-01"
  value={75.5}  // From data
  min={0}       // From schema
  max={100}     // From schema
/>
```

## API Endpoints Used

```
Backend → Frontend Communication

POST /api/dashboard/generate
  Request: { metadata_id: string }
  Response: {
    layout: { type, components },
    metrics: { signal_count, ... },
    generation_context: { strategy, ... }
  }

GET /api/metadata/:id/data
  Response: { T01: 75, P01: 5.2, ... }

GET /api/dashboard/:id
  Response: { id, name, schema, created_at, ... }

POST /api/dashboard
  Request: { name, schema, metadata_id }
  Response: { id, created_at, ... }
```

## Error Scenarios

### Scenario 1: Invalid Metadata
```jsx
const result = await dashboardService.generateDashboard('invalid-id')
// Backend returns 404 or validation error
// Frontend shows error state
```

### Scenario 2: No Components Generated
```json
{
  "layout": {
    "type": "grid",
    "components": []
  }
}
```

### Scenario 3: Data Fetch Fails
```jsx
// Retry with exponential backoff
let retries = 0
const fetchWithRetry = async () => {
  try {
    return await fetch(url).then(r => r.json())
  } catch (err) {
    if (retries < 3) {
      retries++
      await new Promise(r => setTimeout(r, 1000 * retries))
      return fetchWithRetry()
    }
    throw err
  }
}
```

## Performance Optimization

```jsx
// Preload components before rendering
import { preloadComponents } from '@/schema-renderer'

useEffect(() => {
  // Preload all possible component types
  preloadComponents([
    'temperature_gauge',
    'pressure_gauge',
    'trend_chart',
    'alarm_banner',
    'metric_card'
  ])
}, [])

// Lazy load non-critical components
const TrendChart = lazy(() => import('@/widgets/TrendChart'))
```

## Caching Strategy

```javascript
// Cache generated schemas
const schemaCache = new Map()

async function getCachedSchema(metadataId) {
  if (schemaCache.has(metadataId)) {
    return schemaCache.get(metadataId)
  }

  const schema = await dashboardService.generateDashboard(metadataId)
  schemaCache.set(metadataId, schema)

  // Clear cache after 1 hour
  setTimeout(() => schemaCache.delete(metadataId), 3600000)

  return schema
}
```

## Summary

The Schema-Driven Rendering System perfectly complements the Backend Dashboard Generation Engine:

1. **Backend** generates intelligent schemas from industrial metadata
2. **Frontend** renders those schemas to interactive React dashboards
3. **Data layer** provides real-time sensor values
4. **Result** is a complete, automated dashboard pipeline

No manual component wiring needed - everything is declarative and data-driven.

---

**Next**: See [README.md](./README.md) for detailed API reference
**Examples**: Check [EXAMPLES.jsx](./EXAMPLES.jsx) for more patterns
