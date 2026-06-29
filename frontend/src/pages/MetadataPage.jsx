/**
 * Metadata/Systems Page
 * 
 * Manage industrial systems and metadata
 */

import { useState } from 'react'
import { useFetch } from '../hooks/useFetch'
import metadataService from '../services/metadata'
import dashboardService from '../services/dashboard'
import LoadingSpinner from '../components/LoadingSpinner'
import Alert from '../components/Alert'
import Button from '../components/Button'
import { Plus, Zap, Trash2 } from 'lucide-react'

export default function MetadataPage() {
  const { data: systems, loading, error, retry } = useFetch(() =>
    metadataService.listMetadata(0, 50)
  )
  const [generating, setGenerating] = useState(null)

  const handleGenerateDashboard = async (id) => {
    setGenerating(id)
    try {
      await dashboardService.generateDashboard(id)
      // Success - could show toast or redirect
    } catch (err) {
      console.error('Failed to generate dashboard:', err)
    } finally {
      setGenerating(null)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
    return (
      <Alert
        type="error"
        title="Failed to load systems"
        message={error.message}
      />
    )
  }

  const systemResults = systems?.results || systems || []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Industrial Systems</h1>
          <p className="text-gray-600 mt-2">
            Manage your industrial systems and generate dashboards
          </p>
        </div>
        <Button variant="primary" size="lg">
          <Plus className="w-5 h-5 mr-2" />
          Add System
        </Button>
      </div>

      {/* Systems List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">System</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Type</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Sensors</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {systemResults.length > 0 ? (
              systemResults.map((system) => (
                <tr key={system.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div>
                      <p className="font-medium text-gray-900">{system.name}</p>
                      <p className="text-sm text-gray-600">{system.code}</p>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {system.system_type || 'N/A'}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">
                    {system.sensors?.length || 0}
                  </td>
                  <td className="px-6 py-4 text-sm space-x-2">
                    <Button
                      variant="secondary"
                      size="sm"
                      loading={generating === system.id}
                      onClick={() => handleGenerateDashboard(system.id)}
                    >
                      <Zap className="w-4 h-4 mr-1" />
                      Generate
                    </Button>
                    <Button
                      variant="danger"
                      size="sm"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="px-6 py-8 text-center text-gray-600">
                  No systems found. Add a new system to get started.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
