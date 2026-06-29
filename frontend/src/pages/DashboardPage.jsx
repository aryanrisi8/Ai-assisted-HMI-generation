/**
 * Dashboard Page
 * 
 * Main dashboard with system overview
 */

import { useFetch } from '../hooks/useFetch'
import { Link } from 'react-router-dom'
import dashboardService from '../services/dashboard'
import LoadingSpinner from '../components/LoadingSpinner'
import Alert from '../components/Alert'
import Button from '../components/Button'
import { BarChart3, TrendingUp, AlertCircle, PlusCircle } from 'lucide-react'

export default function DashboardPage() {
  const { data: dashboards, loading, error } = useFetch(() =>
    dashboardService.listDashboards(0, 10)
  )

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
        title="Failed to load dashboards"
        message={error.message}
      />
    )
  }

  const dashboardResults = dashboards?.results || dashboards || []

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Overview of your industrial systems and monitoring dashboards
        </p>
      </div>

      {/* Stats */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600">Active Systems</p>
              <p className="text-3xl font-bold text-gray-900">12</p>
            </div>
            <BarChart3 className="w-12 h-12 text-primary-600 opacity-10" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600">Signals Monitored</p>
              <p className="text-3xl font-bold text-gray-900">342</p>
            </div>
            <TrendingUp className="w-12 h-12 text-primary-600 opacity-10" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600">Active Alarms</p>
              <p className="text-3xl font-bold text-red-600">3</p>
            </div>
            <AlertCircle className="w-12 h-12 text-red-600 opacity-10" />
          </div>
        </div>
      </div>

      {/* Recent Dashboards */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">Recent Dashboards</h2>
          </div>
          <Link to="/dashboard/editor">
            <Button variant="primary" size="sm">
              <PlusCircle className="w-4 h-4 mr-2" /> New dashboard
            </Button>
          </Link>
        </div>
        <div className="divide-y divide-gray-200">
          {dashboardResults.length > 0 ? (
            dashboardResults.map((dashboard) => (
              <div key={dashboard.id} className="p-6 flex items-center justify-between hover:bg-gray-50">
                <div>
                  <p className="font-medium text-gray-900">{dashboard.name}</p>
                  <p className="text-sm text-gray-600">
                    Updated {new Date(dashboard.updated_at).toLocaleDateString()}
                  </p>
                </div>
                <Link
                  to={`/dashboard/editor/${dashboard.id}`}
                  className="inline-flex items-center px-4 py-2 text-primary-600 hover:bg-primary-50 rounded-lg"
                >
                  Edit
                </Link>
              </div>
            ))
          ) : (
            <div className="p-6 text-center text-gray-600">
              No dashboards yet. Create your first dashboard to get started.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
