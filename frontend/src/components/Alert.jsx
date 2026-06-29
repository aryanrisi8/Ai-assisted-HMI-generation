/**
 * Alert Component
 * 
 * Displays alerts for errors, info, success, warning
 */

import { AlertCircle, CheckCircle, AlertTriangle, Info, X } from 'lucide-react'
import { useState, useEffect } from 'react'

export default function Alert({ type = 'info', message, title, closeable = true, autoClose = 5000 }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    if (autoClose && visible) {
      const timer = setTimeout(() => setVisible(false), autoClose)
      return () => clearTimeout(timer)
    }
  }, [autoClose, visible])

  if (!visible) return null

  const styles = {
    error: 'bg-red-50 border-red-200 text-red-800',
    success: 'bg-green-50 border-green-200 text-green-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    info: 'bg-blue-50 border-blue-200 text-blue-800',
  }

  const icons = {
    error: <AlertCircle className="w-5 h-5" />,
    success: <CheckCircle className="w-5 h-5" />,
    warning: <AlertTriangle className="w-5 h-5" />,
    info: <Info className="w-5 h-5" />,
  }

  return (
    <div className={`flex items-start space-x-3 p-4 rounded-lg border ${styles[type]}`}>
      {icons[type]}
      <div className="flex-1">
        {title && <h3 className="font-semibold">{title}</h3>}
        <p className="text-sm">{message}</p>
      </div>
      {closeable && (
        <button
          onClick={() => setVisible(false)}
          className="flex-shrink-0"
        >
          <X className="w-5 h-5" />
        </button>
      )}
    </div>
  )
}
