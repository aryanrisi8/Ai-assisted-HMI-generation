/**
 * Metric Card Component
 * Displays a single metric with status indicator and optional trend
 */

import React from 'react'
import { TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react'

const MetricCard = ({
  title = 'Metric',
  value = 0,
  unit = '',
  status = 'normal', // 'normal', 'warning', 'critical'
  trend = null, // { value: number, percentage: number, direction: 'up' | 'down' }
  description = '',
  showWarningThreshold = true,
  warningThreshold = null,
  showCriticalThreshold = true,
  criticalThreshold = null,
  showTrend = true,
  showHistory = false,
  history = [], // Array of { timestamp, value }
  icon: CustomIcon = null,
  onClick = null,
  actionLabel = null,
  onAction = null,
}) => {
  // Determine status color
  const getStatusColor = () => {
    switch (status) {
      case 'critical':
        return { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', badge: 'bg-red-100 text-red-800', dot: 'bg-red-500' }
      case 'warning':
        return { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-700', badge: 'bg-yellow-100 text-yellow-800', dot: 'bg-yellow-500' }
      default:
        return { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-700', badge: 'bg-blue-100 text-blue-800', dot: 'bg-blue-500' }
    }
  }

  const statusColor = getStatusColor()

  // Calculate trend visualization
  const trendColor = trend?.direction === 'up' ? 'text-red-500' : 'text-green-500'
  const TrendIcon = trend?.direction === 'up' ? TrendingUp : TrendingDown

  // Mini history chart
  const renderHistoryChart = () => {
    if (!showHistory || history.length === 0) return null

    const chartData = history.slice(-20) // Last 20 points
    if (chartData.length === 0) return null

    const values = chartData.map((h) => h.value)
    const minVal = Math.min(...values)
    const maxVal = Math.max(...values)
    const range = maxVal - minVal || 1

    const points = chartData.map((h, idx) => {
      const x = (idx / (chartData.length - 1 || 1)) * 100
      const y = 100 - ((h.value - minVal) / range) * 100
      return `${x},${y}`
    })

    const pathD = `M ${points.join(' L ')}`

    return (
      <svg width="100%" height="40" viewBox="0 0 100 40" preserveAspectRatio="none" className="mt-3">
        <path d={pathD} stroke={statusColor.dot} strokeWidth="0.5" fill="none" />
      </svg>
    )
  }

  return (
    <div
      className={`p-6 rounded-lg border-2 cursor-pointer transition-all hover:shadow-lg ${statusColor.bg} ${statusColor.border}`}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3 flex-1">
          {CustomIcon && <CustomIcon size={24} className={statusColor.text} />}
          <div>
            <h3 className="text-sm font-semibold text-gray-800">{title}</h3>
            {description && <p className="text-xs text-gray-600 mt-1">{description}</p>}
          </div>
        </div>

        {/* Status badge */}
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${statusColor.dot}`} />
          <span className={`px-2 py-1 text-xs font-medium rounded-full ${statusColor.badge} capitalize`}>
            {status}
          </span>
        </div>
      </div>

      {/* Main value */}
      <div className="mb-4">
        <div className="flex items-baseline gap-1">
          <span className={`text-3xl font-bold ${statusColor.text}`}>
            {typeof value === 'number' ? value.toFixed(2) : value}
          </span>
          {unit && <span className="text-sm text-gray-600">{unit}</span>}
        </div>
      </div>

      {/* Trend */}
      {showTrend && trend && (
        <div className="mb-3 flex items-center gap-2">
          <TrendIcon size={16} className={trendColor} />
          <span className={`text-sm font-medium ${trendColor}`}>
            {trend.direction === 'up' ? '+' : ''}
            {trend.value.toFixed(2)} ({trend.percentage?.toFixed(1)}%)
          </span>
        </div>
      )}

      {/* Thresholds */}
      <div className="space-y-2 mb-3 text-xs">
        {showWarningThreshold && warningThreshold !== null && (
          <div className="flex justify-between text-yellow-700">
            <span>Warning:</span>
            <span>{warningThreshold}</span>
          </div>
        )}
        {showCriticalThreshold && criticalThreshold !== null && (
          <div className="flex justify-between text-red-700">
            <span>Critical:</span>
            <span>{criticalThreshold}</span>
          </div>
        )}
      </div>

      {/* History chart */}
      {renderHistoryChart()}

      {/* Action button */}
      {onAction && actionLabel && (
        <button
          onClick={(e) => {
            e.stopPropagation()
            onAction()
          }}
          className={`w-full mt-4 px-3 py-2 text-sm font-medium rounded transition-colors ${
            status === 'critical'
              ? 'bg-red-200 hover:bg-red-300 text-red-800'
              : status === 'warning'
                ? 'bg-yellow-200 hover:bg-yellow-300 text-yellow-800'
                : 'bg-blue-200 hover:bg-blue-300 text-blue-800'
          }`}
        >
          {actionLabel}
        </button>
      )}

      {/* Alert icon for critical */}
      {status === 'critical' && (
        <div className="absolute top-4 right-4">
          <AlertTriangle size={20} className="text-red-500 animate-pulse" />
        </div>
      )}
    </div>
  )
}

export default MetricCard
