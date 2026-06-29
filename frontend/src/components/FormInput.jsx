/**
 * Form Components
 * 
 * Reusable form input components
 */

export function FormInput({
  label,
  type = 'text',
  error,
  required = false,
  className = '',
  ...props
}) {
  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <input
        type={type}
        className={`
          w-full px-4 py-2 rounded-lg border
          ${error ? 'border-red-300 focus:ring-red-500' : 'border-gray-300 focus:ring-primary-500'}
          focus:outline-none focus:ring-2
          transition
          ${className}
        `}
        {...props}
      />
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  )
}

export function FormTextarea({
  label,
  error,
  required = false,
  className = '',
  ...props
}) {
  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <textarea
        className={`
          w-full px-4 py-2 rounded-lg border
          ${error ? 'border-red-300 focus:ring-red-500' : 'border-gray-300 focus:ring-primary-500'}
          focus:outline-none focus:ring-2
          transition
          ${className}
        `}
        {...props}
      />
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  )
}

export function FormSelect({
  label,
  error,
  required = false,
  options = [],
  className = '',
  ...props
}) {
  return (
    <div className="space-y-1">
      {label && (
        <label className="block text-sm font-medium text-gray-700">
          {label}
          {required && <span className="text-red-500">*</span>}
        </label>
      )}
      <select
        className={`
          w-full px-4 py-2 rounded-lg border
          ${error ? 'border-red-300 focus:ring-red-500' : 'border-gray-300 focus:ring-primary-500'}
          focus:outline-none focus:ring-2
          transition
          ${className}
        `}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  )
}
