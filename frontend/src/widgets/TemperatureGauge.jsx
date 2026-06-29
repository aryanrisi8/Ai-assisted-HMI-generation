/**
 * Temperature Gauge Component
 * Displays temperature with circular gauge visualization
 */

import React, { useState, useEffect } from 'react'
import { Thermometer } from 'lucide-react'

const TemperatureGauge = ({
  value = 0,
  min = 0,
  max = 100,
  unit = '°C',
  threshold = null,
  showScale = true,
  showValue = true,
  warning = null,
  critical = null,
  animated = true,
  title = 'Temperature',
  onThresholdExceeded = null,
}) => {
  const [displayValue, setDisplayValue] = useState(value)

  useEffect(() => {
    if (animated) {
      const interval = setInterval(() => {
        setDisplayValue((prev) => {
          const diff = value - prev
          if (Math.abs(diff) < 0.1) return value
          return prev + diff * 0.1
        })
      }, 50)
      return () => clearInterval(interval)
    } else {
      setDisplayValue(value)
    }
  }, [value, animated])

  // Calculate position on gauge (0-360 degrees)
  const percentage = (displayValue - min) / (max - min)
  const rotation = Math.max(0, Math.min(360, percentage * 360))

  // Determine color based on threshold
  let valueColor = '#3b82f6' // blue
  let statusText = 'Normal'
  if (critical !== null && displayValue >= critical) {
    valueColor = '#dc2626' // red
    statusText = 'Critical'
    if (onThresholdExceeded) onThresholdExceeded({ type: 'critical', value: displayValue })
  } else if (warning !== null && displayValue >= warning) {
    valueColor = '#f59e0b' // amber
    statusText = 'Warning'
    if (onThresholdExceeded) onThresholdExceeded({ type: 'warning', value: displayValue })
  }

  return (
    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <Thermometer size={24} className="text-blue-500" />
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      </div>

      {/* Gauge SVG */}
      <svg width="200" height="200" viewBox="0 0 200 200" className="mb-4">
        {/* Background circle */}
        <circle cx="100" cy="100" r="90" fill="none" stroke="#e5e7eb" strokeWidth="2" />

        {/* Scale marks */}
        {showScale &&
          Array.from({ length: 13 }).map((_, i) => {
            const angle = (i / 12) * 360 - 90
            const x1 = 100 + 85 * Math.cos((angle * Math.PI) / 180)
            const y1 = 100 + 85 * Math.sin((angle * Math.PI) / 180)
            const x2 = 100 + 75 * Math.cos((angle * Math.PI) / 180)
            const y2 = 100 + 75 * Math.sin((angle * Math.PI) / 180)
            return (
              <line
                key={i}
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke="#9ca3af"
                strokeWidth="1"
              />
            )
          })}

        {/* Value arc */}
        <path
          d={`M ${100 + 80 * Math.cos(((-90) * Math.PI) / 180)} ${
            100 + 80 * Math.sin(((-90) * Math.PI) / 180)
          } A 80 80 0 ${rotation > 180 ? 1 : 0} 1 ${100 + 80 * Math.cos(((rotation - 90) * Math.PI) / 180)} ${
            100 + 80 * Math.sin(((rotation - 90) * Math.PI) / 180)
          }`}
          fill="none"
          stroke={valueColor}
          strokeWidth="8"
          strokeLinecap="round"
        />

        {/* Needle */}
        <line
          x1="100"
          y1="100"
          x2={100 + 60 * Math.cos(((rotation - 90) * Math.PI) / 180)}
          y2={100 + 60 * Math.sin(((rotation - 90) * Math.PI) / 180)}
          stroke={valueColor}
          strokeWidth="3"
          strokeLinecap="round"
        />

        {/* Center circle */}
        <circle cx="100" cy="100" r="5" fill={valueColor} />

        {/* Value text */}
        {showValue && (
          <>
            <text x="100" y="120" textAnchor="middle" className="text-2xl font-bold fill-gray-800">
              {displayValue.toFixed(1)}
            </text>
            <text x="100" y="135" textAnchor="middle" className="text-sm fill-gray-600">
              {unit}
            </text>
          </>
        )}
      </svg>

      {/* Status indicator */}
      <div className="flex items-center gap-2">
        <div
          className="w-3 h-3 rounded-full"
          style={{ backgroundColor: valueColor }}
        />
        <span className="text-sm font-medium" style={{ color: valueColor }}>
          {statusText}
        </span>
      </div>

      {/* Range display */}
      {showScale && (
        <div className="mt-4 text-xs text-gray-600 text-center">
          Range: {min}{unit} - {max}{unit}
          {warning !== null && ` | Warning: {warning}{unit}`}
          {critical !== null && ` | Critical: {critical}{unit}`}
        </div>
      )}
    </div>
  )
}

export default TemperatureGauge
