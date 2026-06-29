/**
 * Schema Renderer Engine
 * Converts JSON schemas into React component trees
 * 
 * Purpose:
 * - Transforms dashboard JSON schemas into renderable components
 * - Handles component resolution and instantiation
 * - Supports nested layouts and compositions
 * - Provides error recovery and fallbacks
 */

import React from 'react'
import { getComponentByType, getDefaultProps, validateComponentSchema } from './registry'

/**
 * Render a single component from schema
 * 
 * @param {object} componentSchema - Schema for single component
 *   {
 *     type: 'temperature_gauge',
 *     id: 'temp-sensor-1',
 *     props: { value: 75, min: 0, max: 100 },
 *     children: [] (optional)
 *   }
 * @param {object} context - Rendering context and callbacks
 * @returns {React.Element} Rendered component
 */
export const renderComponent = (componentSchema, context = {}) => {
  if (!componentSchema) {
    return null
  }

  // Validate schema
  const validation = validateComponentSchema(componentSchema)
  if (!validation.valid) {
    console.error('Invalid component schema:', validation.errors, componentSchema)
    if (context.onError) {
      context.onError(new Error(validation.errors.join(', ')))
    }
    return null
  }

  // Get component from registry
  const Component = getComponentByType(componentSchema.type)
  if (!Component) {
    console.error(`Component type "${componentSchema.type}" not found`)
    if (context.onError) {
      context.onError(new Error(`Component type "${componentSchema.type}" not found`))
    }
    return <MissingComponent type={componentSchema.type} schema={componentSchema} />
  }

  // Merge default props with provided props
  const defaultProps = getDefaultProps(componentSchema.type)
  const props = {
    ...defaultProps,
    ...componentSchema.props,
    key: componentSchema.id || componentSchema.type,
  }

  // Add context callbacks
  if (context.onComponentRender) {
    context.onComponentRender(componentSchema)
  }

  // Render with error boundary
  try {
    return <Component {...props} />
  } catch (error) {
    console.error('Error rendering component:', error, componentSchema)
    if (context.onError) {
      context.onError(error)
    }
    return <ComponentError error={error} schema={componentSchema} />
  }
}

/**
 * Render multiple components from schema array
 * 
 * @param {array} componentsSchema - Array of component schemas
 * @param {object} context - Rendering context
 * @returns {array} Array of rendered components
 */
export const renderComponents = (componentsSchema, context = {}) => {
  if (!Array.isArray(componentsSchema)) {
    return []
  }

  return componentsSchema
    .map((schema, index) => renderComponent(schema, context))
    .filter((component) => component !== null)
}

/**
 * Render layout with components
 * 
 * @param {object} layoutSchema - Layout schema
 *   {
 *     type: 'grid',
 *     columns: 3,
 *     gap: 4,
 *     components: [...]
 *   }
 * @param {object} context - Rendering context
 * @returns {React.Element} Rendered layout
 */
export const renderLayout = (layoutSchema, context = {}) => {
  if (!layoutSchema) {
    return null
  }

  const { type = 'grid', columns = 1, gap = 4, components = [] } = layoutSchema

  if (type === 'grid') {
    return (
      <div className={`grid grid-cols-${columns} gap-${gap}`}>
        {renderComponents(components, context)}
      </div>
    )
  }

  if (type === 'flex') {
    const { direction = 'row', wrap = true, justify = 'start', align = 'stretch' } = layoutSchema
    return (
      <div className={`flex flex-${direction} ${wrap ? 'flex-wrap' : 'flex-nowrap'} justify-${justify} items-${align}`}>
        {renderComponents(components, context)}
      </div>
    )
  }

  if (type === 'stack') {
    return (
      <div className="flex flex-col gap-4">
        {renderComponents(components, context)}
      </div>
    )
  }

  // Default to components list
  return <>{renderComponents(components, context)}</>
}

/**
 * Render complete dashboard from schema
 * 
 * @param {object} dashboardSchema - Complete dashboard schema
 *   {
 *     version: '1.0',
 *     title: 'Dashboard Name',
 *     layout: { type: 'grid', columns: 3, components: [...] }
 *   }
 * @param {object} context - Rendering context and callbacks
 * @returns {React.Element} Rendered dashboard
 */
export const renderDashboard = (dashboardSchema, context = {}) => {
  if (!dashboardSchema) {
    return <div className="p-4 text-red-600">No schema provided</div>
  }

  const { version = '1.0', title, description, layout = {}, components = [] } = dashboardSchema

  // Determine what to render
  let content = null
  if (layout && layout.components && layout.components.length > 0) {
    content = renderLayout(layout, context)
  } else if (components && components.length > 0) {
    content = renderComponents(components, context)
  } else {
    content = <div className="p-4 text-gray-500">No components to render</div>
  }

  return (
    <div className="w-full">
      {title && <h1 className="text-3xl font-bold mb-4">{title}</h1>}
      {description && <p className="text-gray-600 mb-6">{description}</p>}
      {content}
    </div>
  )
}

/**
 * Transform data into component-ready format
 * Maps raw data to component props
 * 
 * @param {object} data - Raw data
 * @param {object} transformConfig - Transformation configuration
 * @returns {object} Transformed props
 */
export const transformData = (data, transformConfig = {}) => {
  if (!transformConfig.mapping) {
    return data
  }

  return Object.entries(transformConfig.mapping).reduce((acc, [key, mapping]) => {
    if (typeof mapping === 'string') {
      // Simple path mapping: 'temperature' -> 'sensor.temp'
      acc[key] = getDataByPath(data, mapping)
    } else if (typeof mapping === 'function') {
      // Custom transform function
      acc[key] = mapping(data)
    } else if (typeof mapping === 'object') {
      // Complex mapping with options
      acc[key] = getDataByPath(data, mapping.path, mapping.default)
    }
    return acc
  }, {})
}

/**
 * Get nested data by path
 * @param {object} obj - Object to traverse
 * @param {string} path - Dot-separated path (e.g., 'sensor.temperature.current')
 * @param {any} defaultValue - Default value if path not found
 * @returns {any} Data at path or default
 */
export const getDataByPath = (obj, path, defaultValue = null) => {
  if (!path || !obj) return defaultValue

  const keys = path.split('.')
  let current = obj

  for (const key of keys) {
    if (current && typeof current === 'object' && key in current) {
      current = current[key]
    } else {
      return defaultValue
    }
  }

  return current
}

/**
 * Merge schemas (for composition/inheritance)
 * @param {object} baseSchema - Base schema
 * @param {object} overrideSchema - Override schema
 * @returns {object} Merged schema
 */
export const mergeSchemas = (baseSchema, overrideSchema) => {
  return {
    ...baseSchema,
    ...overrideSchema,
    layout: {
      ...baseSchema.layout,
      ...overrideSchema.layout,
      components: [...(baseSchema.layout?.components || []), ...(overrideSchema.layout?.components || [])],
    },
  }
}

// Error Components

/**
 * Fallback component for missing component types
 */
const MissingComponent = ({ type, schema }) => (
  <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-md">
    <p className="text-yellow-800 font-semibold">Missing Component</p>
    <p className="text-yellow-700 text-sm">Type: {type}</p>
    <details className="mt-2">
      <summary className="cursor-pointer text-yellow-600 text-sm">Schema</summary>
      <pre className="mt-2 p-2 bg-white rounded text-xs overflow-auto">
        {JSON.stringify(schema, null, 2)}
      </pre>
    </details>
  </div>
)

/**
 * Error component for rendering failures
 */
const ComponentError = ({ error, schema }) => (
  <div className="p-4 bg-red-50 border border-red-200 rounded-md">
    <p className="text-red-800 font-semibold">Rendering Error</p>
    <p className="text-red-700 text-sm">{error?.message || 'Unknown error'}</p>
    <details className="mt-2">
      <summary className="cursor-pointer text-red-600 text-sm">Details</summary>
      <pre className="mt-2 p-2 bg-white rounded text-xs overflow-auto text-red-600">
        {error?.stack || 'No stack trace'}
      </pre>
    </details>
  </div>
)

export default {
  renderComponent,
  renderComponents,
  renderLayout,
  renderDashboard,
  transformData,
  getDataByPath,
  mergeSchemas,
}
