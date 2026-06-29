/**
 * Component Registry
 * Maps component type strings to React components
 * 
 * Purpose:
 * - Central registry of all renderable components
 * - Allows dynamic component resolution
 * - Supports lazy loading and custom components
 * - Provides introspection capabilities
 */

import TemperatureGauge from '../widgets/TemperatureGauge'
import PressureGauge from '../widgets/PressureGauge'
import TrendChart from '../widgets/TrendChart'
import AlarmBanner from '../widgets/AlarmBanner'
import MetricCard from '../widgets/MetricCard'

/**
 * Core component registry
 * Maps component type strings to React components
 */
const COMPONENT_REGISTRY = {
  temperature_gauge: {
    component: TemperatureGauge,
    displayName: 'Temperature Gauge',
    version: '1.0.0',
    category: 'gauge',
    description: 'Displays temperature with gauge visualization',
    defaultProps: {
      min: 0,
      max: 100,
      unit: '°C',
      showScale: true,
      showValue: true,
      threshold: null,
    },
  },

  pressure_gauge: {
    component: PressureGauge,
    displayName: 'Pressure Gauge',
    version: '1.0.0',
    category: 'gauge',
    description: 'Displays pressure with gauge visualization',
    defaultProps: {
      min: 0,
      max: 10,
      unit: 'bar',
      showScale: true,
      showValue: true,
      threshold: null,
    },
  },

  trend_chart: {
    component: TrendChart,
    displayName: 'Trend Chart',
    version: '1.0.0',
    category: 'chart',
    description: 'Time-series line chart for trending data',
    defaultProps: {
      timeRange: '1h',
      showLegend: true,
      showGrid: true,
      showTooltip: true,
      colors: ['#3b82f6', '#ef4444', '#10b981'],
    },
  },

  alarm_banner: {
    component: AlarmBanner,
    displayName: 'Alarm Banner',
    version: '1.0.0',
    category: 'alert',
    description: 'Displays active alarms and alerts',
    defaultProps: {
      showBorder: true,
      showIcon: true,
      sound: false,
      autoClose: false,
      maxAlarms: 5,
    },
  },

  metric_card: {
    component: MetricCard,
    displayName: 'Metric Card',
    version: '1.0.0',
    category: 'card',
    description: 'Displays a single metric with status indicator',
    defaultProps: {
      showWarningThreshold: true,
      showCriticalThreshold: true,
      showTrend: true,
      showHistory: false,
    },
  },
}

/**
 * Get component by type
 * @param {string} type - Component type identifier
 * @returns {object} Component metadata and React component
 */
export const getComponent = (type) => {
  const entry = COMPONENT_REGISTRY[type]
  if (!entry) {
    console.warn(`Component type "${type}" not found in registry`)
    return null
  }
  return entry
}

/**
 * Get React component directly
 * @param {string} type - Component type identifier
 * @returns {React.Component} React component
 */
export const getComponentByType = (type) => {
  const entry = getComponent(type)
  return entry ? entry.component : null
}

/**
 * Check if component type is registered
 * @param {string} type - Component type identifier
 * @returns {boolean} True if registered
 */
export const isComponentRegistered = (type) => {
  return type in COMPONENT_REGISTRY
}

/**
 * Get all registered components
 * @returns {object} All component entries
 */
export const getAllComponents = () => {
  return { ...COMPONENT_REGISTRY }
}

/**
 * Get component metadata
 * @param {string} type - Component type identifier
 * @returns {object} Metadata (displayName, version, category, etc.)
 */
export const getComponentMetadata = (type) => {
  const entry = getComponent(type)
  if (!entry) return null
  
  const { component, ...metadata } = entry
  return metadata
}

/**
 * Get components by category
 * @param {string} category - Category name
 * @returns {object} Components in category
 */
export const getComponentsByCategory = (category) => {
  return Object.entries(COMPONENT_REGISTRY).reduce((acc, [type, entry]) => {
    if (entry.category === category) {
      acc[type] = entry
    }
    return acc
  }, {})
}

/**
 * Get default props for component type
 * @param {string} type - Component type identifier
 * @returns {object} Default props
 */
export const getDefaultProps = (type) => {
  const entry = getComponent(type)
  return entry ? { ...entry.defaultProps } : {}
}

/**
 * Register custom component
 * @param {string} type - Component type identifier
 * @param {React.Component} component - React component
 * @param {object} metadata - Component metadata
 */
export const registerComponent = (type, component, metadata = {}) => {
  if (type in COMPONENT_REGISTRY) {
    console.warn(`Component type "${type}" already registered. Overwriting.`)
  }

  COMPONENT_REGISTRY[type] = {
    component,
    displayName: metadata.displayName || type,
    version: metadata.version || '1.0.0',
    category: metadata.category || 'custom',
    description: metadata.description || '',
    defaultProps: metadata.defaultProps || {},
    ...metadata,
  }
}

/**
 * Unregister component
 * @param {string} type - Component type identifier
 */
export const unregisterComponent = (type) => {
  delete COMPONENT_REGISTRY[type]
}

/**
 * Get all available component types
 * @returns {string[]} Array of component type identifiers
 */
export const getAvailableTypes = () => {
  return Object.keys(COMPONENT_REGISTRY)
}

/**
 * Validate component schema against registry
 * @param {object} schema - Component schema
 * @returns {object} Validation result { valid: boolean, errors: string[] }
 */
export const validateComponentSchema = (schema) => {
  const errors = []

  if (!schema) {
    errors.push('Schema is required')
    return { valid: false, errors }
  }

  if (!schema.type) {
    errors.push('Component type is required')
  } else if (!isComponentRegistered(schema.type)) {
    errors.push(`Component type "${schema.type}" is not registered`)
  }

  if (schema.id && typeof schema.id !== 'string') {
    errors.push('Component id must be a string')
  }

  if (schema.props && typeof schema.props !== 'object') {
    errors.push('Component props must be an object')
  }

  return {
    valid: errors.length === 0,
    errors,
  }
}

export default COMPONENT_REGISTRY
