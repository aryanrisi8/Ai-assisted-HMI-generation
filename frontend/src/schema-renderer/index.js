/**
 * Schema Renderer Module
 * Complete schema-driven rendering system for React dashboards
 * 
 * Exports:
 * - Registry: Component registration and management
 * - Engine: Schema rendering and transformation
 * - Loader: Dynamic component loading
 */

export {
  getComponent,
  getComponentByType,
  isComponentRegistered,
  getAllComponents,
  getComponentMetadata,
  getComponentsByCategory,
  getDefaultProps,
  registerComponent,
  unregisterComponent,
  getAvailableTypes,
  validateComponentSchema,
} from './registry'

export {
  renderComponent,
  renderComponents,
  renderLayout,
  renderDashboard,
  transformData,
  getDataByPath,
  mergeSchemas,
} from './engine'

export {
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
} from './loader'

export { default as SchemaRenderer } from './SchemaRenderer'
