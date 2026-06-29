/**
 * Alarm Banner Component
 * Displays active alarms and alerts with severity levels
 */

import React, { useState, useEffect } from 'react'
import {
  AlertCircle,
  AlertTriangle,
  Bell,
  X,
  Volume2,
} from 'lucide-react'

const AlarmBanner = ({
  title = 'Active Alarms',
  alarms = [],
  showBorder = true,
  showIcon = true,
  sound = false,
  autoClose = false,
  autoCloseDuration = 5000,
  maxAlarms = 5,
  onAlarmClick = null,
  onAlarmDismiss = null,
  onPlaySound = null,
}) => {
  const [visibleAlarms, setVisibleAlarms] = useState(alarms.slice(0, maxAlarms))
  const [dismissedAlarms, setDismissedAlarms] = useState(new Set())

  // Update alarms
  useEffect(() => {
    const active = alarms
      .filter((a) => !dismissedAlarms.has(a.id))
      .slice(0, maxAlarms)
    setVisibleAlarms(active)

    // Play sound if enabled and new alarm
    if (sound && alarms.length > visibleAlarms.length && onPlaySound) {
      onPlaySound()
    }
  }, [alarms, dismissedAlarms, maxAlarms, sound, visibleAlarms.length, onPlaySound])

  // Auto-close alarms
  useEffect(() => {
    if (!autoClose) return

    const timer = setTimeout(() => {
      if (visibleAlarms.length > 0) {
        const firstAlarm = visibleAlarms[0]
        handleDismiss(firstAlarm.id)
      }
    }, autoCloseDuration)

    return () => clearTimeout(timer)
  }, [visibleAlarms, autoClose, autoCloseDuration])

  const handleDismiss = (id) => {
    const newDismissed = new Set(dismissedAlarms)
    newDismissed.add(id)
    setDismissedAlarms(newDismissed)

    if (onAlarmDismiss) {
      const alarm = alarms.find((a) => a.id === id)
      if (alarm) onAlarmDismiss(alarm)
    }
  }

  const handleAlarmClick = (alarm) => {
    if (onAlarmClick) {
      onAlarmClick(alarm)
    }
  }

  // Severity levels
  const getSeverityStyle = (severity = 'info') => {
    const styles = {
      critical: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-800', icon: '#dc2626' },
      warning: { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-800', icon: '#f59e0b' },
      info: { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-800', icon: '#3b82f6' },
      success: { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-800', icon: '#10b981' },
    }
    return styles[severity] || styles.info
  }

  const totalAlarms = alarms.length
  const hasOverflow = totalAlarms > maxAlarms

  return (
    <div className="w-full space-y-2">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          {showIcon && <Bell size={20} className="text-red-500" />}
          <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
          {totalAlarms > 0 && (
            <span className="inline-flex items-center justify-center w-6 h-6 ml-2 text-xs font-bold text-white bg-red-500 rounded-full">
              {totalAlarms}
            </span>
          )}
        </div>

        {sound && (
          <button
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Sound enabled"
          >
            <Volume2 size={18} className="text-gray-600" />
          </button>
        )}
      </div>

      {/* Alarms list */}
      <div className="space-y-2">
        {visibleAlarms.length === 0 ? (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-800 text-sm font-medium">✓ No active alarms</p>
          </div>
        ) : (
          visibleAlarms.map((alarm, idx) => {
            const style = getSeverityStyle(alarm.severity)
            const Icon = alarm.severity === 'critical' ? AlertCircle : AlertTriangle

            return (
              <div
                key={alarm.id || idx}
                className={`p-4 border rounded-lg ${style.bg} ${showBorder ? style.border : ''} cursor-pointer hover:shadow-md transition-shadow`}
                onClick={() => handleAlarmClick(alarm)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-1">
                    {showIcon && (
                      <Icon size={18} className="mt-1 flex-shrink-0" style={{ color: style.icon }} />
                    )}

                    <div className="flex-1 min-w-0">
                      <h4 className={`font-semibold ${style.text} truncate`}>
                        {alarm.title || 'Unnamed Alarm'}
                      </h4>

                      {alarm.message && (
                        <p className={`text-sm mt-1 ${style.text} opacity-85 line-clamp-2`}>
                          {alarm.message}
                        </p>
                      )}

                      <div className="flex items-center gap-4 mt-2 text-xs opacity-75 flex-wrap">
                        {alarm.timestamp && (
                          <span>
                            {new Date(alarm.timestamp).toLocaleTimeString()}
                          </span>
                        )}
                        {alarm.source && (
                          <span className="px-2 py-1 bg-black bg-opacity-10 rounded">
                            {alarm.source}
                          </span>
                        )}
                        {alarm.severity && (
                          <span className="px-2 py-1 bg-black bg-opacity-10 rounded capitalize">
                            {alarm.severity}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Dismiss button */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      handleDismiss(alarm.id)
                    }}
                    className="ml-2 p-1 opacity-50 hover:opacity-100 transition-opacity"
                    title="Dismiss alarm"
                  >
                    <X size={16} />
                  </button>
                </div>
              </div>
            )
          })
        )}
      </div>

      {/* Overflow indicator */}
      {hasOverflow && (
        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
          <p className="text-sm text-gray-700">
            +{totalAlarms - maxAlarms} more alarm{totalAlarms - maxAlarms !== 1 ? 's' : ''}
          </p>
        </div>
      )}

      {/* Actions */}
      {visibleAlarms.length > 0 && (
        <div className="flex gap-2 mt-4">
          <button
            onClick={() => setDismissedAlarms(new Set(alarms.map((a) => a.id)))}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            Dismiss All
          </button>
        </div>
      )}
    </div>
  )
}

export default AlarmBanner
