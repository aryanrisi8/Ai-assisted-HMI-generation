/**
 * Trend Chart Component
 * Displays time-series line chart for trending data
 */

import React, { useMemo } from 'react'
import { TrendingUp } from 'lucide-react'

const TrendChart = ({
  title = 'Trend Chart',
  data = [],
  series = [],
  timeRange = '1h',
  showLegend = true,
  showGrid = true,
  showTooltip = true,
  colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b'],
  height = 300,
  interactive = true,
}) => {
  // Validate and prepare data
  const chartData = useMemo(() => {
    if (!data || data.length === 0) {
      return []
    }

    // If data is simple array of numbers, convert to objects
    if (typeof data[0] === 'number') {
      return data.map((value, index) => ({
        timestamp: index,
        value,
      }))
    }

    return data
  }, [data])

  // Prepare series configuration
  const seriesConfig = useMemo(() => {
    if (series.length > 0) return series

    // Auto-detect series from data
    if (chartData.length === 0) return []

    const firstRow = chartData[0]
    const keys = Object.keys(firstRow).filter((k) => k !== 'timestamp' && typeof firstRow[k] === 'number')

    return keys.map((key, idx) => ({
      key,
      label: key,
      color: colors[idx % colors.length],
    }))
  }, [series, chartData, colors])

  // Calculate scales
  const { minY, maxY } = useMemo(() => {
    if (chartData.length === 0) return { minY: 0, maxY: 100 }

    let min = Infinity
    let max = -Infinity

    chartData.forEach((row) => {
      seriesConfig.forEach((s) => {
        const value = row[s.key]
        if (typeof value === 'number') {
          min = Math.min(min, value)
          max = Math.max(max, value)
        }
      })
    })

    if (min === max) {
      min = max - 10
    }

    const padding = (max - min) * 0.1
    return { minY: min - padding, maxY: max + padding }
  }, [chartData, seriesConfig])

  // Canvas dimensions
  const width = 100
  const chartHeight = height - 60
  const padding = { top: 20, right: 20, bottom: 40, left: 50 }

  const chartWidth = width - padding.left - padding.right
  const chartAreaHeight = chartHeight - padding.top - padding.bottom

  // Generate path for line
  const generatePath = (serieKey) => {
    if (chartData.length === 0) return ''

    const points = chartData.map((row, idx) => {
      const x = padding.left + (idx / (chartData.length - 1 || 1)) * chartWidth
      const value = row[serieKey] || 0
      const y = padding.top + chartAreaHeight - ((value - minY) / (maxY - minY)) * chartAreaHeight
      return `${x},${y}`
    })

    return `M ${points.join(' L ')}`
  }

  // Render
  return (
    <div className="flex flex-col p-6 bg-white rounded-lg shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <TrendingUp size={24} className="text-blue-500" />
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
        <span className="text-xs text-gray-500 ml-auto">{timeRange}</span>
      </div>

      {/* Chart container */}
      <svg
        width="100%"
        height={chartHeight}
        viewBox={`0 0 ${width} ${chartHeight}`}
        className="border border-gray-200 rounded"
        preserveAspectRatio="xMidYMid meet"
      >
        {/* Grid */}
        {showGrid && (
          <g stroke="#e5e7eb" strokeWidth="0.5">
            {/* Horizontal grid lines */}
            {Array.from({ length: 5 }).map((_, i) => {
              const y = padding.top + (i / 4) * chartAreaHeight
              return (
                <line
                  key={`h${i}`}
                  x1={padding.left}
                  y1={y}
                  x2={width - padding.right}
                  y2={y}
                />
              )
            })}

            {/* Vertical grid lines */}
            {Array.from({ length: Math.min(10, chartData.length) }).map((_, i) => {
              const x = padding.left + (i / Math.max(1, Math.min(10, chartData.length) - 1)) * chartWidth
              return (
                <line
                  key={`v${i}`}
                  x1={x}
                  y1={padding.top}
                  x2={x}
                  y2={chartHeight - padding.bottom}
                />
              )
            })}
          </g>
        )}

        {/* Y-axis labels */}
        {Array.from({ length: 5 }).map((_, i) => {
          const value = minY + (i / 4) * (maxY - minY)
          const y = padding.top + chartAreaHeight - (i / 4) * chartAreaHeight
          return (
            <text
              key={`ylbl${i}`}
              x={padding.left - 10}
              y={y}
              textAnchor="end"
              dy="0.3em"
              className="text-xs fill-gray-600"
            >
              {value.toFixed(0)}
            </text>
          )
        })}

        {/* Y-axis */}
        <line
          x1={padding.left}
          y1={padding.top}
          x2={padding.left}
          y2={chartHeight - padding.bottom}
          stroke="#9ca3af"
          strokeWidth="1"
        />

        {/* X-axis */}
        <line
          x1={padding.left}
          y1={chartHeight - padding.bottom}
          x2={width - padding.right}
          y2={chartHeight - padding.bottom}
          stroke="#9ca3af"
          strokeWidth="1"
        />

        {/* Data lines */}
        {seriesConfig.map((s, idx) => (
          <g key={`series${idx}`}>
            <path
              d={generatePath(s.key)}
              fill="none"
              stroke={s.color}
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* Data points */}
            {chartData.map((row, dataIdx) => {
              const value = row[s.key]
              if (typeof value !== 'number') return null
              const x = padding.left + (dataIdx / (chartData.length - 1 || 1)) * chartWidth
              const y = padding.top + chartAreaHeight - ((value - minY) / (maxY - minY)) * chartAreaHeight
              return (
                <circle
                  key={`point${idx}${dataIdx}`}
                  cx={x}
                  cy={y}
                  r="3"
                  fill={s.color}
                  opacity="0.6"
                />
              )
            })}
          </g>
        ))}
      </svg>

      {/* Legend */}
      {showLegend && seriesConfig.length > 0 && (
        <div className="flex gap-4 mt-4 flex-wrap">
          {seriesConfig.map((s, idx) => (
            <div key={idx} className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded"
                style={{ backgroundColor: s.color }}
              />
              <span className="text-sm text-gray-700">{s.label}</span>
            </div>
          ))}
        </div>
      )}

      {/* Empty state */}
      {chartData.length === 0 && (
        <div className="flex items-center justify-center h-48 text-gray-500">
          <p>No data available</p>
        </div>
      )}
    </div>
  )
}

export default TrendChart
