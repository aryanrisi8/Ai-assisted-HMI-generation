/**
 * Error handling utilities
 */

/**
 * Format API error message
 */
export function getErrorMessage(error) {
  if (error?.response?.data?.detail) {
    return error.response.data.detail
  }
  if (error?.message) {
    return error.message
  }
  return 'An error occurred'
}

/**
 * Format API error for display
 */
export function formatApiError(error) {
  const statusCode = error?.response?.status
  const detail = getErrorMessage(error)

  if (statusCode === 400) {
    return `Validation error: ${detail}`
  }
  if (statusCode === 401) {
    return 'Unauthorized - please log in'
  }
  if (statusCode === 403) {
    return 'Forbidden - you do not have permission'
  }
  if (statusCode === 404) {
    return 'Not found'
  }
  if (statusCode === 500) {
    return 'Server error - please try again'
  }

  return detail || 'An unexpected error occurred'
}

/**
 * Check if error is network error
 */
export function isNetworkError(error) {
  return !error?.response || error.code === 'ECONNABORTED'
}
