/**
 * Dashboard Editor Page
 *
 * Visual editor for dashboard layouts using React Grid Layout.
 * Supports drag, resize, add/delete widgets, save to backend, and live preview.
 */

import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { Plus, Save, Trash2, ArrowLeft, LayoutGrid } from 'lucide-react'
import RGL, { WidthProvider } from 'react-grid-layout'
import 'react-grid-layout/css/styles.css'
import 'react-resizable/css/styles.css'

import dashboardService from '../services/dashboard'
import { getAllComponents, getComponentMetadata, getDefaultProps } from '../schema-renderer/registry'
import { renderDashboard } from '../schema-renderer/engine'
import Button from '../components/Button'
import LoadingSpinner from '../components/LoadingSpinner'
import Alert from '../components/Alert'

const GridLayout = WidthProvider(RGL)

function createDefaultWidget(type) {
  const metadata = getComponentMetadata(type) || {}
  const uid = `${type}-${Date.now()}`

  return {
    id: uid,
    type,
    title: metadata.displayName || type,
    props: getDefaultProps(type),
    layout: {
      i: uid,
      x: 0,
      y: Infinity,
      w: 4,
      h: 5,
    },
  }
}

function buildPreviewSchema(name, description, columns, items) {
  return {
    title: name || 'Dashboard preview',
    description,
    layout: {
      type: 'grid',
      columns,
      gap: 6,
      components: items.map((item) => ({
        id: item.id,
        type: item.type,
        props: item.props,
      })),
    },
  }
}

export default function DashboardEditorPage() {
  const navigate = useNavigate()
  const { dashboardId } = useParams()
  const [dashboard, setDashboard] = useState(null)
  const [name, setName] = useState('Untitled Dashboard')
  const [description, setDescription] = useState('')
  const [metadataId, setMetadataId] = useState('')
  const [widgets, setWidgets] = useState([])
  const [saving, setSaving] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [message, setMessage] = useState(null)

  const availableWidgetTypes = useMemo(
    () => Object.keys(getAllComponents()),
    []
  )
  const [selectedWidgetType, setSelectedWidgetType] = useState(
    availableWidgetTypes[0] || 'metric_card'
  )

  useEffect(() => {
    if (!dashboardId) return

    setLoading(true)
    dashboardService
      .getDashboard(dashboardId)
      .then((result) => {
        if (result && result.dashboard) {
          setDashboard(result.dashboard)
          setName(result.dashboard.name)
          setDescription(result.dashboard.description || '')
          setMetadataId(result.dashboard.industrial_system_id || '')
          const layoutPayload = result.layout?.layout_json || result.layout
          const items = (layoutPayload?.components || []).map((component) => ({
            id: component.id,
            type: component.type,
            title: component.title || getComponentMetadata(component.type)?.displayName || component.type,
            props: component.props || {},
            layout: {
              ...component.layout,
              i: component.id,
            },
          }))
          setWidgets(items)
        }
      })
      .catch((err) => {
        setError(err)
      })
      .finally(() => setLoading(false))
  }, [dashboardId])

  const handleAddWidget = () => {
    const widget = createDefaultWidget(selectedWidgetType)
    setWidgets((current) => [...current, widget])
  }

  const handleRemoveWidget = (id) => {
    setWidgets((current) => current.filter((item) => item.id !== id))
  }

  const handleLayoutChange = (newLayout) => {
    setWidgets((current) =>
      current.map((item) => {
        const nextLayout = newLayout.find((layoutItem) => layoutItem.i === item.id)
        if (!nextLayout) {
          return item
        }
        return {
          ...item,
          layout: {
            ...item.layout,
            ...nextLayout,
          },
        }
      })
    )
  }

  const handleSave = async () => {
    setSaving(true)
    setError(null)
    setMessage(null)

    const layoutPayload = {
      breakpoint: 'lg',
      columns: 12,
      row_height: 30,
      components: widgets.map((item) => ({
        id: item.id,
        type: item.type,
        title: item.title,
        props: item.props,
        layout: item.layout,
      })),
    }

    try {
      if (dashboardId) {
        await dashboardService.updateDashboard(dashboardId, {
          name,
          description,
          metadata_id: metadataId || null,
          layout: layoutPayload,
        })
        setMessage('Dashboard updated successfully.')
      } else {
        const created = await dashboardService.saveDashboard({
          name,
          description,
          metadata_id: metadataId || null,
          layout: layoutPayload,
        })
        setDashboard(created.dashboard)
        navigate(`/dashboard/editor/${created.dashboard.id}`)
        setMessage('Dashboard created successfully.')
      }
    } catch (err) {
      setError(err)
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner />
      </div>
    )
  }

  const previewSchema = buildPreviewSchema(
    name,
    description,
    12,
    widgets
  )

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard Editor</h1>
          <p className="text-gray-600 mt-2">
            Build and persist dashboard layouts using drag & drop widgets.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Link to="/dashboard" className="inline-flex items-center gap-2 text-gray-700 hover:text-primary-600">
            <ArrowLeft className="w-4 h-4" /> Back to dashboards
          </Link>
          <Button variant="secondary" onClick={() => setWidgets([])}>
            <Trash2 className="w-4 h-4 mr-2" /> Clear canvas
          </Button>
          <Button variant="primary" onClick={handleSave} loading={saving}>
            <Save className="w-4 h-4 mr-2" /> Save dashboard
          </Button>
        </div>
      </div>

      {error && (
        <Alert
          type="error"
          title="Unable to save dashboard"
          message={error.message || 'Please try again.'}
        />
      )}
      {message && (
        <Alert
          type="success"
          title="Saved"
          message={message}
        />
      )}

      <div className="grid lg:grid-cols-[1.5fr_1fr] gap-6">
        <section className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="grid gap-4 md:grid-cols-2">
              <label className="space-y-2">
                <span className="text-sm font-medium text-gray-700">Dashboard name</span>
                <input
                  type="text"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary-500 focus:outline-none"
                />
              </label>
              <label className="space-y-2">
                <span className="text-sm font-medium text-gray-700">Linked metadata</span>
                <input
                  type="text"
                  value={metadataId}
                  onChange={(event) => setMetadataId(event.target.value)}
                  placeholder="Metadata ID"
                  className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary-500 focus:outline-none"
                />
              </label>
            </div>
            <label className="space-y-2 mt-4">
              <span className="text-sm font-medium text-gray-700">Description</span>
              <textarea
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                rows="3"
                className="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary-500 focus:outline-none"
              />
            </label>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Widget palette</h2>
                <p className="text-sm text-gray-600">Add components and customize the editor canvas.</p>
              </div>
              <Button variant="secondary" onClick={handleAddWidget}>
                <Plus className="w-4 h-4 mr-2" /> Add widget
              </Button>
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              <select
                value={selectedWidgetType}
                onChange={(event) => setSelectedWidgetType(event.target.value)}
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-2 focus:border-primary-500 focus:outline-none"
              >
                {availableWidgetTypes.map((widgetType) => (
                  <option key={widgetType} value={widgetType}>
                    {getComponentMetadata(widgetType)?.displayName || widgetType}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Canvas</h2>
                <p className="text-sm text-gray-600">Drag and resize widgets to build the final dashboard.</p>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <LayoutGrid className="w-4 h-4" /> {widgets.length} widgets
              </div>
            </div>
            <div className="min-h-[500px] rounded-xl border border-dashed border-gray-300 bg-gray-50 p-2">
              <GridLayout
                className="layout"
                layout={widgets.map((item) => item.layout)}
                cols={12}
                rowHeight={30}
                width={1200}
                onLayoutChange={handleLayoutChange}
                draggableHandle=".drag-handle"
              >
                {widgets.map((item) => (
                  <div key={item.id} className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
                    <div className="flex items-center justify-between mb-3 drag-handle cursor-move text-gray-600">
                      <span className="font-medium">{item.title}</span>
                      <button
                        type="button"
                        onClick={() => handleRemoveWidget(item.id)}
                        className="rounded-lg bg-red-50 px-2 py-1 text-red-600 hover:bg-red-100"
                      >
                        Remove
                      </button>
                    </div>
                    <div className="text-sm text-gray-500">
                      Type: {item.type}
                    </div>
                  </div>
                ))}
              </GridLayout>
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Live preview</h2>
            <div className="space-y-4">
              {widgets.length === 0 ? (
                <div className="rounded-lg border border-dashed border-gray-300 bg-gray-50 p-6 text-center text-gray-500">
                  Add widgets to see a live preview.
                </div>
              ) : (
                <div className="space-y-4">
                  {renderDashboard(previewSchema)}
                </div>
              )}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Inspector</h2>
            <p className="text-sm text-gray-600">
              Pick a widget and edit properties in the sidebar. You can also remove widgets from the canvas.
            </p>
          </div>
        </aside>
      </div>
    </div>
  )
}
