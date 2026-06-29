/**
 * Schema-Driven Rendering Examples
 * Complete usage patterns and real-world scenarios
 */

// ============================================================================
// EXAMPLE 1: Basic Dashboard Rendering
// ============================================================================

import SchemaRenderer from '@/schema-renderer'

export function BasicDashboard() {
  const schema = {
    version: '1.0',
    title: 'Industrial Monitor',
    description: 'Real-time sensor monitoring',
    layout: {
      type: 'grid',
      columns: 3,
      gap: 4,
      components: [
        {
          id: 'temp-gauge',
          type: 'temperature_gauge',
          props: {
            title: 'Reactor Temperature',
            value: 75,
            min: 0,
            max: 100,
            unit: '°C',
            warning: 80,
            critical: 90,
            showScale: true,
            showValue: true,
          },
        },
        {
          id: 'pressure-gauge',
          type: 'pressure_gauge',
          props: {
            title: 'System Pressure',
            value: 5.5,
            min: 0,
            max: 10,
            unit: 'bar',
            warning: 8,
            critical: 9,
          },
        },
        {
          id: 'alarms',
          type: 'alarm_banner',
          props: {
            title: 'Active Alarms',
            maxAlarms: 5,
            showBorder: true,
          },
        },
      ],
    },
  }

  return <SchemaRenderer schema={schema} />
}

// ============================================================================
// EXAMPLE 2: Dynamic Data with Transformation
// ============================================================================

import { useState, useEffect } from 'react'
import { transformData } from '@/schema-renderer'

export function DynamicDashboard() {
  const [sensorData, setSensorData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Fetch real sensor data
    const fetchData = async () => {
      try {
        const response = await fetch('/api/sensors')
        const data = await response.json()
        setSensorData(data)
      } catch (error) {
        console.error('Failed to fetch sensor data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    // Refetch every 5 seconds
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  const schema = {
    title: 'Live Sensor Dashboard',
    components: [
      {
        id: 'temp-gauge',
        type: 'temperature_gauge',
        props: {
          title: 'Temperature',
          // Value will be filled by transformation
          min: 0,
          max: 100,
          unit: '°C',
        },
      },
      {
        id: 'pressure-gauge',
        type: 'pressure_gauge',
        props: {
          title: 'Pressure',
          min: 0,
          max: 10,
          unit: 'bar',
        },
      },
    ],
  }

  // Transform API response to component props
  const transformedData = sensorData
    ? transformData(sensorData, {
        mapping: {
          'temperature_gauge.value': 'sensors.temperature.current',
          'pressure_gauge.value': 'sensors.pressure.current',
        },
      })
    : null

  return (
    <SchemaRenderer
      schema={schema}
      data={transformedData}
      loading={loading}
      onError={(error) => console.error('Render error:', error)}
    />
  )
}

// ============================================================================
// EXAMPLE 3: Multi-Series Trend Chart
// ============================================================================

export function TrendDashboard() {
  const historicalData = [
    { timestamp: 0, temperature: 20, humidity: 45, pressure: 1.0 },
    { timestamp: 1, temperature: 22, humidity: 48, pressure: 1.1 },
    { timestamp: 2, temperature: 25, humidity: 50, pressure: 1.2 },
    { timestamp: 3, temperature: 28, humidity: 52, pressure: 1.3 },
    { timestamp: 4, temperature: 30, humidity: 55, pressure: 1.4 },
    { timestamp: 5, temperature: 32, humidity: 58, pressure: 1.5 },
  ]

  const schema = {
    title: '24-Hour Environment Analysis',
    layout: {
      type: 'stack',
      components: [
        {
          id: 'trend-chart',
          type: 'trend_chart',
          props: {
            title: 'Environment Trends',
            data: historicalData,
            series: [
              { key: 'temperature', label: 'Temperature (°C)', color: '#ef4444' },
              { key: 'humidity', label: 'Humidity (%)', color: '#3b82f6' },
              { key: 'pressure', label: 'Pressure (bar)', color: '#10b981' },
            ],
            timeRange: '24h',
            showLegend: true,
            showGrid: true,
            height: 400,
          },
        },
      ],
    },
  }

  return <SchemaRenderer schema={schema} />
}

// ============================================================================
// EXAMPLE 4: Alarm Management Dashboard
// ============================================================================

export function AlarmDashboard() {
  const activeAlarms = [
    {
      id: 'alarm-1',
      title: 'High Temperature Alert',
      message: 'Reactor temperature exceeded warning threshold (85°C)',
      severity: 'warning',
      source: 'REACTOR-01',
      timestamp: new Date(Date.now() - 5 * 60000), // 5 min ago
    },
    {
      id: 'alarm-2',
      title: 'Critical Pressure',
      message: 'System pressure critical level (9.8 bar)',
      severity: 'critical',
      source: 'PUMP-02',
      timestamp: new Date(Date.now() - 2 * 60000), // 2 min ago
    },
    {
      id: 'alarm-3',
      title: 'Low Flow Rate',
      message: 'Main pump flow below minimum threshold',
      severity: 'warning',
      source: 'PUMP-01',
      timestamp: new Date(Date.now() - 30000), // 30 sec ago
    },
  ]

  const schema = {
    title: 'Alarm Center',
    layout: {
      type: 'stack',
      components: [
        {
          id: 'alarms',
          type: 'alarm_banner',
          props: {
            title: 'Active Alarms',
            alarms: activeAlarms,
            showBorder: true,
            showIcon: true,
            sound: false,
            autoClose: false,
            maxAlarms: 10,
          },
        },
      ],
    },
  }

  return (
    <SchemaRenderer
      schema={schema}
      onError={(error) => console.error('Error rendering alarms:', error)}
    />
  )
}

// ============================================================================
// EXAMPLE 5: Metrics Dashboard with Multiple Components
// ============================================================================

export function MetricsDashboard() {
  const metrics = [
    {
      id: 'metric-1',
      title: 'CPU Usage',
      value: 67.5,
      unit: '%',
      status: 'normal',
      trend: { value: 2.3, percentage: 4.2, direction: 'up' },
    },
    {
      id: 'metric-2',
      title: 'Memory',
      value: 8342,
      unit: 'MB',
      status: 'warning',
      trend: { value: 156, percentage: 1.9, direction: 'up' },
    },
    {
      id: 'metric-3',
      title: 'Network I/O',
      value: 2456.8,
      unit: 'Mbps',
      status: 'normal',
      trend: { value: -123.4, percentage: -4.8, direction: 'down' },
    },
    {
      id: 'metric-4',
      title: 'Disk Usage',
      value: 456,
      unit: 'GB',
      status: 'critical',
      trend: { value: 45, percentage: 10.9, direction: 'up' },
    },
  ]

  const schema = {
    title: 'System Metrics',
    layout: {
      type: 'grid',
      columns: 4,
      gap: 4,
      components: metrics.map((m) => ({
        id: m.id,
        type: 'metric_card',
        props: {
          title: m.title,
          value: m.value,
          unit: m.unit,
          status: m.status,
          trend: m.trend,
          showTrend: true,
          showWarningThreshold: true,
          warningThreshold: 80,
          showCriticalThreshold: true,
          criticalThreshold: 95,
        },
      })),
    },
  }

  return <SchemaRenderer schema={schema} />
}

// ============================================================================
// EXAMPLE 6: Custom Component at Runtime
// ============================================================================

import { registerCustomComponent, loadComponent } from '@/schema-renderer'

// Define custom gauge component
function CustomGaugeComponent({ title, value, min, max }) {
  return (
    <div className="p-6 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg text-white">
      <h3 className="text-lg font-bold mb-4">{title}</h3>
      <div className="text-4xl font-bold mb-2">{value}</div>
      <div className="w-full bg-white rounded-full h-2">
        <div
          className="bg-gradient-to-r from-yellow-400 to-red-500 h-2 rounded-full"
          style={{ width: `${((value - min) / (max - min)) * 100}%` }}
        />
      </div>
      <div className="mt-2 text-xs opacity-75">Range: {min} - {max}</div>
    </div>
  )
}

export function CustomComponentDashboard() {
  // Register custom component
  registerCustomComponent('custom_gauge', CustomGaugeComponent, {
    displayName: 'Custom Gauge',
    category: 'visualization',
    description: 'Beautiful gradient gauge component',
  })

  const schema = {
    title: 'Dashboard with Custom Component',
    layout: {
      type: 'grid',
      columns: 2,
      gap: 4,
      components: [
        {
          id: 'custom-1',
          type: 'custom_gauge',
          props: {
            title: 'Performance',
            value: 75,
            min: 0,
            max: 100,
          },
        },
        {
          id: 'temp-gauge',
          type: 'temperature_gauge',
          props: {
            title: 'Temperature',
            value: 65,
          },
        },
      ],
    },
  }

  return <SchemaRenderer schema={schema} />
}

// ============================================================================
// EXAMPLE 7: Async Data with useSchemaRenderer Hook
// ============================================================================

import { useSchemaRenderer } from '@/schema-renderer'

export function AsyncDashboard() {
  const baseSchema = {
    title: 'Real-time Monitoring',
    components: [
      {
        id: 'temperature',
        type: 'temperature_gauge',
        props: { title: 'Current Temperature' },
      },
      {
        id: 'pressure',
        type: 'pressure_gauge',
        props: { title: 'System Pressure' },
      },
    ],
  }

  // Use hook for automatic data fetching
  const { data, loading, error, refetch } = useSchemaRenderer(
    baseSchema,
    async () => {
      const response = await fetch('/api/realtime-data')
      if (!response.ok) throw new Error('Failed to fetch')
      return response.json()
    }
  )

  return (
    <SchemaRenderer
      schema={baseSchema}
      data={data}
      loading={loading}
      error={error?.message}
      refetch={refetch}
    />
  )
}

// ============================================================================
// EXAMPLE 8: Complex Multi-Layout Dashboard
// ============================================================================

export function ComplexDashboard() {
  const schema = {
    title: 'Comprehensive Industrial Control Dashboard',
    version: '1.0',
    layout: {
      type: 'grid',
      columns: 12,
      gap: 4,
      components: [
        // Alarms - full width
        {
          id: 'alarms',
          type: 'alarm_banner',
          props: { title: 'Critical Alerts', maxAlarms: 5 },
        },
        // Gauges - left column
        {
          id: 'temp-1',
          type: 'temperature_gauge',
          props: { title: 'Reactor 1', value: 75 },
        },
        {
          id: 'temp-2',
          type: 'temperature_gauge',
          props: { title: 'Reactor 2', value: 82 },
        },
        // Chart - middle
        {
          id: 'trend',
          type: 'trend_chart',
          props: { title: '24h Data', height: 400 },
        },
        // Metrics - right column
        {
          id: 'metric-1',
          type: 'metric_card',
          props: {
            title: 'Throughput',
            value: 1250,
            unit: 'units/hr',
            status: 'normal',
          },
        },
        {
          id: 'metric-2',
          type: 'metric_card',
          props: {
            title: 'Efficiency',
            value: 94.2,
            unit: '%',
            status: 'normal',
          },
        },
      ],
    },
  }

  return <SchemaRenderer schema={schema} />
}

// ============================================================================
// EXAMPLE 9: Schema Validation
// ============================================================================

import { validateComponentSchema, getAvailableTypes } from '@/schema-renderer'

export function SchemaValidationExample() {
  const invalidSchema = {
    id: 'invalid',
    type: 'unknown_component', // Not registered!
    props: {},
  }

  const validation = validateComponentSchema(invalidSchema)

  if (!validation.valid) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded">
        <h3 className="font-bold text-red-800 mb-2">Schema Validation Failed</h3>
        <ul className="list-disc list-inside text-red-700">
          {validation.errors.map((err, idx) => (
            <li key={idx}>{err}</li>
          ))}
        </ul>
        <p className="mt-4 text-sm text-gray-600">
          Available types: {getAvailableTypes().join(', ')}
        </p>
      </div>
    )
  }

  return <div className="text-green-600">Schema is valid!</div>
}

// ============================================================================
// EXAMPLE 10: Component Registry Inspection
// ============================================================================

import {
  getAllComponents,
  getComponentsByCategory,
  getComponentMetadata,
  getAvailableTypes,
} from '@/schema-renderer'

export function RegistryInspectionExample() {
  const allComponents = getAllComponents()
  const gauges = getComponentsByCategory('gauge')
  const types = getAvailableTypes()

  return (
    <div className="space-y-6 p-6 bg-white rounded-lg">
      <div>
        <h3 className="font-bold mb-2">Available Components</h3>
        <div className="space-y-2">
          {types.map((type) => {
            const metadata = getComponentMetadata(type)
            return (
              <div key={type} className="p-3 bg-gray-50 rounded">
                <p className="font-medium">{metadata.displayName}</p>
                <p className="text-sm text-gray-600">{metadata.description}</p>
                <p className="text-xs text-gray-500">Category: {metadata.category}</p>
              </div>
            )
          })}
        </div>
      </div>

      <div>
        <h3 className="font-bold mb-2">Gauge Components</h3>
        <pre className="bg-gray-100 p-2 rounded text-xs overflow-auto">
          {JSON.stringify(Object.keys(gauges), null, 2)}
        </pre>
      </div>
    </div>
  )
}

// ============================================================================
// EXAMPLE 11: Error Handling
// ============================================================================

export function ErrorHandlingExample() {
  const [errors, setErrors] = useState([])

  const schema = {
    components: [
      { id: 'valid', type: 'temperature_gauge', props: {} },
      { id: 'invalid', type: 'unknown_type', props: {} },
    ],
  }

  return (
    <SchemaRenderer
      schema={schema}
      onError={(error) => {
        setErrors((prev) => [...prev, error])
      }}
      onComponentRender={(schema) => {
        console.log(`Rendered: ${schema.id}`)
      }}
    />
  )
}

// ============================================================================
// EXAMPLE 12: Export/Import Dashboard Configuration
// ============================================================================

export function DashboardConfigManager() {
  const dashboard = {
    version: '1.0',
    title: 'Saved Configuration',
    lastModified: new Date().toISOString(),
    layout: {
      type: 'grid',
      columns: 3,
      gap: 4,
      components: [
        {
          id: 'temp-gauge',
          type: 'temperature_gauge',
          props: { title: 'Temperature', value: 75 },
        },
        {
          id: 'pressure-gauge',
          type: 'pressure_gauge',
          props: { title: 'Pressure', value: 5.5 },
        },
      ],
    },
  }

  // Export (download)
  const exportConfig = () => {
    const json = JSON.stringify(dashboard, null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'dashboard-config.json'
    a.click()
  }

  // Import (upload and validate)
  const importConfig = (file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const imported = JSON.parse(e.target.result)
        // Validate
        if (imported.layout?.components) {
          console.log('Valid configuration imported')
        }
      } catch (error) {
        console.error('Invalid JSON format')
      }
    }
    reader.readAsText(file)
  }

  return (
    <div className="space-y-4 p-6">
      <button
        onClick={exportConfig}
        className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
      >
        Export Configuration
      </button>

      <label className="block">
        <span className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 cursor-pointer inline-block">
          Import Configuration
        </span>
        <input
          type="file"
          accept=".json"
          onChange={(e) => e.target.files[0] && importConfig(e.target.files[0])}
          className="hidden"
        />
      </label>

      <pre className="bg-gray-100 p-4 rounded overflow-auto">
        {JSON.stringify(dashboard, null, 2)}
      </pre>
    </div>
  )
}

export default {
  BasicDashboard,
  DynamicDashboard,
  TrendDashboard,
  AlarmDashboard,
  MetricsDashboard,
  CustomComponentDashboard,
  AsyncDashboard,
  ComplexDashboard,
  SchemaValidationExample,
  RegistryInspectionExample,
  ErrorHandlingExample,
  DashboardConfigManager,
}
