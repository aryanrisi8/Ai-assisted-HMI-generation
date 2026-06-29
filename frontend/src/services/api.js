/**
 * API Service Layer
 * 
 * Centralized HTTP client with:
 * - Automatic token injection
 * - Error handling
 * - Request/response interceptors
 * - Timeout management
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 30000

/**
 * Create and configure the axios instance
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Request interceptor - Add auth token
 */
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

/**
 * Response interceptor - Handle errors and token refresh
 */
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

/**
 * Export configured API methods
 */
export default apiClient
