/**
 * Pressure Gauge Component
 * Displays pressure with circular gauge visualization
 */

import React, { useState, useEffect } from 'react'
import { Gauge } from 'lucide-react'

const PressureGauge = ({
  value = 0,
  min = 0,
  max = 10,
  unit = 'bar',
  threshold = null,
  showScale = true,
  showValue = true,
  warning = null,
  critical = null,
  animated = true,
  title = 'Pressure',
  onThresholdExceeded = null,
}) => {
  const [displayValue, setDisplayValue] = useState(value)

  useEffect(() => {
    if (animated) {
      const interval = setInterval(() => {
        setDisplayValue((prev) => {
          const diff = value - prev
          if (Math.abs(diff) < 0.01) return value
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
  let valueColor = '#10b981' // green
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

  // Zone colors for background
  const zones = [
    { start: 0, end: 5, color: '#dcfce7', label: 'Low' },
    { start: 5, end: 8, color: '#f0fdf4', label: 'Normal' },
    { start: 8, end: 10, color: '#fef3c7', label: 'High' },
  ]

  return (
    <div className="flex flex-col items-center p-6 bg-white rounded-lg shadow-md">
      <div className="flex items-center gap-2 mb-4">
        <Gauge size={24} className="text-green-500" />
        <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
      </div>

      {/* Gauge SVG */}
      <svg width="220" height="220" viewBox="0 0 220 220" className="mb-4">
        {/* Background zones */}
        {zones.map((zone, idx) => {
          const startAngle = ((zone.start / max) * 360 - 90) * (Math.PI / 180)
          const endAngle = ((zone.end / max) * 360 - 90) * (Math.PI / 180)
          const x1 = 110 + 85 * Math.cos(startAngle)
          const y1 = 110 + 85 * Math.sin(startAngle)
          const x2 = 110 + 85 * Math.cos(endAngle)
          const y2 = 110 + 85 * Math.sin(endAngle)

          return (
            <g key={idx} opacity="0.3">
              <path
                d={`M 110 110 L ${x1} ${y1} A 85 85 0 0 1 ${x2} ${y2} Z`}
                fill={zone.color}
              />
            </g>
          )
        })}

        {/* Main circle */}
        <circle cx="110" cy="110" r="95" fill="none" stroke="#e5e7eb" strokeWidth="2" />

        {/* Critical zone indicator */}
        {critical !== null && (
          <path
            d={`M ${110 + 85 * Math.cos((((critical / max) * 360 - 90) * Math.PI) / 180)} ${
              110 + 85 * Math.sin((((critical / max) * 360 - 90) * Math.PI) / 180)
            } L ${110 + 75 * Math.cos((((critical / max) * 360 - 90) * Math.PI) / 180)} ${
              110 + 75 * Math.sin((((critical / max) * 360 - 90) * Math.PI) / 180)
            }`}
            stroke="#dc2626"
            strokeWidth="2"
          />
        )}

        {/* Scale marks */}
        {showScale &&
          Array.from({ length: 11 }).map((_, i) => {
            const angle = (i / 10) * 360 - 90
            const x1 = 110 + 90 * Math.cos((angle * Math.PI) / 180)
            const y1 = 110 + 90 * Math.sin((angle * Math.PI) / 180)
            const x2 = 110 + 75 * Math.cos((angle * Math.PI) / 180)
            const y2 = 110 + 75 * Math.sin((angle * Math.PI) / 180)
            return (
              <g key={i}>
                <line
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  stroke="#9ca3af"
                  strokeWidth="2"
                />
                <text
                  x={110 + 60 * Math.cos((angle * Math.PI) / 180)}
                  y={110 + 60 * Math.sin((angle * Math.PI) / 180)}
                  textAnchor="middle"
                  dy="0.3em"
                  className="text-xs fill-gray-600"
                >
                  {(i / 10) * max}
                </text>
              </g>
            )
          })}

        {/* Value arc */}
        <path
          d={`M ${110 + 80 * Math.cos(((-90) * Math.PI) / 180)} ${
            110 + 80 * Math.sin(((-90) * Math.PI) / 180)
          } A 80 80 0 ${rotation > 180 ? 1 : 0} 1 ${110 + 80 * Math.cos(((rotation - 90) * Math.PI) / 180)} ${
            110 + 80 * Math.sin(((rotation - 90) * Math.PI) / 180)
          }`}
          fill="none"
          stroke={valueColor}
          strokeWidth="10"
          strokeLinecap="round"
        />

        {/* Needle */}
        <line
          x1="110"
          y1="110"
          x2={110 + 70 * Math.cos(((rotation - 90) * Math.PI) / 180)}
          y2={110 + 70 * Math.sin(((rotation - 90) * Math.PI) / 180)}
          stroke={valueColor}
          strokeWidth="4"
          strokeLinecap="round"
        />

        {/* Center circle */}
        <circle cx="110" cy="110" r="7" fill={valueColor} />

        {/* Value text */}
        {showValue && (
          <>
            <text x="110" y="135" textAnchor="middle" className="text-3xl font-bold fill-gray-800">
              {displayValue.toFixed(2)}
            </text>
            <text x="110" y="152" textAnchor="middle" className="text-sm fill-gray-600">
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
        </div>
      )}
    </div>
  )
}

export default PressureGauge
