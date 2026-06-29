/**
 * Button Component
 * 
 * Reusable button with variants
 */

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  className = '',
  ...props
}) {
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700 disabled:bg-gray-300',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300 disabled:bg-gray-100',
    danger: 'bg-red-600 text-white hover:bg-red-700 disabled:bg-gray-300',
    outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:text-gray-400',
  }

  const sizes = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      disabled={disabled || loading}
      className={`
        font-medium rounded-lg transition
        ${variants[variant]}
        ${sizes[size]}
        ${disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}
        ${className}
      `}
      {...props}
    >
      {loading ? (
        <div className="flex items-center space-x-2">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"></div>
          <span>Loading...</span>
        </div>
      ) : (
        children
      )}
    </button>
  )
}
