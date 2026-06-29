/**
 * Dynamic Component Loader
 * Asynchronously loads and manages component lifecycle
 * 
 * Purpose:
 * - Code splitting and lazy loading of components
 * - Component caching for performance
 * - Error handling and recovery
 * - Plugin system for custom components
 */

import React, { Suspense, lazy } from 'react'
import { getComponentByType, isComponentRegistered } from './registry'

/**
 * Component cache for lazy-loaded components
 */
const componentCache = new Map()

/**
 * Custom component storage (for runtime registration)
 */
const customComponents = new Map()

/**
 * Loader with suspense wrapper
 * 
 * @param {React.Component} Component - Component to wrap
 * @param {object} fallbackProps - Props for fallback component
 * @returns {React.Element} Wrapped component
 */
const withSuspense = (Component, fallbackProps = {}) => {
  const FallbackComponent = () => (
    <div className="p-4 bg-gray-100 rounded-lg animate-pulse">
      <div className="h-4 bg-gray-300 rounded w-3/4"></div>
    </div>
  )

  return (props) => (
    <Suspense fallback={<FallbackComponent />}>
      <Component {...props} />
    </Suspense>
  )
}

/**
 * Load component by type
 * Supports both registered and custom components
 * 
 * @param {string} type - Component type identifier
 * @param {object} options - Loading options
 *   - useCache: boolean (default: true)
 *   - lazy: boolean (default: false)
 *   - suspense: boolean (default: true)
 * @returns {React.Component} Component class
 */
export const loadComponent = (type, options = {}) => {
  const { useCache = true, lazy: useLazy = false, suspense = true } = options

  // Check cache first
  if (useCache && componentCache.has(type)) {
    return componentCache.get(type)
  }

  // Check custom components
  if (customComponents.has(type)) {
    const Component = customComponents.get(type)
    componentCache.set(type, Component)
    return Component
  }

  // Get from registry
  const Component = getComponentByType(type)
  if (!Component) {
    console.error(`Component "${type}" not found in registry or custom components`)
    return null
  }

  const result = useLazy ? lazy(() => Promise.resolve(Component)) : Component

  const finalComponent = suspense ? withSuspense(result) : result

  // Cache result
  if (useCache) {
    componentCache.set(type, finalComponent)
  }

  return finalComponent
}

/**
 * Preload component
 * Useful for critical path components
 * 
 * @param {string} type - Component type identifier
 * @param {object} options - Loading options
 * @returns {Promise} Resolves when component is preloaded
 */
export const preloadComponent = async (type, options = {}) => {
  const Component = loadComponent(type, { ...options, lazy: false })
  return Component
}

/**
 * Batch preload multiple components
 * 
 * @param {string[]} types - Array of component type identifiers
 * @param {object} options - Loading options
 * @returns {Promise} Resolves when all components are preloaded
 */
export const preloadComponents = async (types, options = {}) => {
  const promises = types.map((type) => preloadComponent(type, options))
  return Promise.all(promises)
}

/**
 * Register custom component at runtime
 * Allows dynamic extension of component library
 * 
 * @param {string} type - Component type identifier
 * @param {React.Component} Component - React component
 * @param {object} options - Registration options
 *   - override: boolean (default: false)
 *   - metadata: object (additional metadata)
 */
export const registerCustomComponent = (type, Component, options = {}) => {
  const { override = false } = options

  if (!override && isComponentRegistered(type)) {
    console.warn(`Component "${type}" already registered. Use override: true to replace.`)
    return false
  }

  if (!override && customComponents.has(type)) {
    console.warn(`Custom component "${type}" already registered. Use override: true to replace.`)
    return false
  }

  customComponents.set(type, Component)

  // Clear cache for this type
  componentCache.delete(type)

  return true
}

/**
 * Unregister custom component
 * 
 * @param {string} type - Component type identifier
 */
export const unregisterCustomComponent = (type) => {
  customComponents.delete(type)
  componentCache.delete(type)
}

/**
 * Clear component cache
 * Useful for hot reloading
 * 
 * @param {string} [type] - Specific type to clear, or all if not specified
 */
export const clearComponentCache = (type) => {
  if (type) {
    componentCache.delete(type)
  } else {
    componentCache.clear()
  }
}

/**
 * Get cache statistics
 * 
 * @returns {object} Cache stats { total, custom, cached }
 */
export const getCacheStats = () => {
  return {
    cached: componentCache.size,
    custom: customComponents.size,
    total: componentCache.size + customComponents.size,
  }
}

/**
 * Check if component can be loaded
 * 
 * @param {string} type - Component type identifier
 * @returns {boolean} True if component can be loaded
 */
export const canLoadComponent = (type) => {
  return isComponentRegistered(type) || customComponents.has(type)
}

/**
 * Get list of loadable components
 * 
 * @returns {string[]} Array of loadable component types
 */
export const getLoadableComponents = () => {
  const registered = Object.keys(require('./registry').getAllComponents())
  const custom = Array.from(customComponents.keys())
  return [...new Set([...registered, ...custom])]
}

/**
 * Lazy load component factory
 * For use with React.lazy()
 * 
 * @param {string} type - Component type identifier
 * @returns {Promise} Resolves to component module
 */
export const lazyLoadComponent = (type) => {
  return new Promise((resolve, reject) => {
    try {
      const Component = getComponentByType(type)
      if (!Component) {
        reject(new Error(`Component "${type}" not found`))
      } else {
        resolve({ default: Component })
      }
    } catch (error) {
      reject(error)
    }
  })
}

/**
 * Get component metadata (for builder UIs, etc)
 * 
 * @param {string} type - Component type identifier
 * @returns {object} Metadata about component
 */
export const getComponentInfo = (type) => {
  const registry = require('./registry')
  const metadata = registry.getComponentMetadata(type)

  return {
    type,
    isRegistered: registry.isComponentRegistered(type),
    isCustom: customComponents.has(type),
    isCached: componentCache.has(type),
    metadata,
  }
}

/**
 * Dynamically create component from schema
 * Complete pipeline: validate -> load -> render
 * 
 * @param {object} schema - Component schema
 * @param {object} options - Loading options
 * @returns {function} Component factory function
 */
export const createComponentFromSchema = (schema, options = {}) => {
  const { type, props = {} } = schema

  const Component = loadComponent(type, options)

  if (!Component) {
    return () => (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <p className="text-red-800 font-semibold">Component not found: {type}</p>
      </div>
    )
  }

  return (additionalProps) => {
    const mergedProps = { ...props, ...additionalProps }
    return <Component {...mergedProps} />
  }
}

/**
 * Component loading context
 * Can be used with Context API for global loader state
 */
export const ComponentLoaderContext = React.createContext({
  loadComponent,
  preloadComponent,
  preloadComponents,
  registerCustomComponent,
  unregisterCustomComponent,
  clearComponentCache,
  canLoadComponent,
  getLoadableComponents,
  getCacheStats,
})

/**
 * Hook for accessing component loader
 * @returns {object} Component loader functions
 */
export const useComponentLoader = () => {
  return React.useContext(ComponentLoaderContext)
}

export default {
  loadComponent,
  preloadComponent,
  preloadComponents,
  registerCustomComponent,
  unregisterCustomComponent,
  clearComponentCache,
  getCacheStats,
  canLoadComponent,
  getLoadableComponents,
  lazyLoadComponent,
  getComponentInfo,
  createComponentFromSchema,
  withSuspense,
  useComponentLoader,
  ComponentLoaderContext,
}
