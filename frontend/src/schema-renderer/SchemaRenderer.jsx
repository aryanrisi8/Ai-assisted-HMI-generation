/**
 * Schema Renderer Component
 * Main wrapper component that renders dashboards from JSON schemas
 * 
 * Usage:
 * <SchemaRenderer schema={dashboardSchema} data={sensorData} />
 */

import React, { useState, useCallback, useMemo } from 'react'
import { renderDashboard, transformData } from './engine'
import { validateComponentSchema } from './registry'

const SchemaRenderer = ({
  schema = null,
  data = null,
  transformConfig = null,
  onError = null,
  onComponentRender = null,
  loading = false,
  error = null,
  refetch = null,
}) => {
  const [renderErrors, setRenderErrors] = useState([])

  // Validate schema
  const schemaValidation = useMemo(() => {
    if (!schema) {
      return { valid: false, errors: ['No schema provided'] }
    }
    return { valid: true, errors: [] }
  }, [schema])

  // Transform data if config provided
  const transformedData = useMemo(() => {
    if (!data || !transformConfig) return data
    return transformData(data, transformConfig)
  }, [data, transformConfig])

  // Prepare rendering context
  const context = useMemo(
    () => ({
      onError: (error) => {
        setRenderErrors((prev) => [...prev, error])
        if (onError) onError(error)
      },
      onComponentRender: (schema) => {
        if (onComponentRender) onComponentRender(schema)
      },
    }),
    [onError, onComponentRender]
  )

  // Handle errors
  const hasErrors = !schemaValidation.valid || renderErrors.length > 0 || !!error

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        <span className="ml-4 text-gray-600">Loading dashboard...</span>
      </div>
    )
  }

  if (hasErrors) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-lg">
        <h2 className="text-lg font-semibold text-red-800 mb-4">Error rendering dashboard</h2>

        {!schemaValidation.valid && (
          <div className="mb-4">
            <h3 className="text-sm font-medium text-red-700 mb-2">Schema Validation Errors:</h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-red-700">
              {schemaValidation.errors.map((err, idx) => (
                <li key={idx}>{err}</li>
              ))}
            </ul>
          </div>
        )}

        {renderErrors.length > 0 && (
          <div className="mb-4">
            <h3 className="text-sm font-medium text-red-700 mb-2">Render Errors ({renderErrors.length}):</h3>
            <div className="space-y-2">
              {renderErrors.map((err, idx) => (
                <div key={idx} className="p-2 bg-white rounded border border-red-200">
                  <p className="text-sm text-red-700 font-mono">{err.message}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="p-3 bg-white rounded border border-red-200">
            <p className="text-sm text-red-700 font-mono">{error}</p>
          </div>
        )}

        {refetch && (
          <button
            onClick={refetch}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        )}
      </div>
    )
  }

  if (!schema) {
    return (
      <div className="p-12 text-center text-gray-500">
        <p>No dashboard schema provided</p>
      </div>
    )
  }

  // Render dashboard
  return (
    <div className="w-full space-y-6">
      {renderDashboard(schema, context)}
    </div>
  )
}

/**
 * Hook for using SchemaRenderer with async data
 */
export const useSchemaRenderer = (schema, dataFetcher, transformConfig) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const refetch = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const result = await dataFetcher()
      setData(result)
    } catch (err) {
      setError(err.message || 'Failed to fetch data')
    } finally {
      setLoading(false)
    }
  }, [dataFetcher])

  // Auto-fetch on mount
  React.useEffect(() => {
    refetch()
  }, [schema, refetch])

  return {
    data,
    loading,
    error,
    refetch,
  }
}

/**
 * Higher-order component for dynamic schema rendering
 */
export const withSchemaRenderer = (Component) => {
  return (props) => {
    const { schema, ...rest } = props

    return (
      <SchemaRenderer schema={schema} {...rest}>
        <Component schema={schema} {...rest} />
      </SchemaRenderer>
    )
  }
}

export default SchemaRenderer
