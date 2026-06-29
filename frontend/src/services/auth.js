/**
 * Authentication Service
 * 
 * API calls for:
 * - Login/logout
 * - User registration
 * - Token refresh
 * - User profile
 */

import apiClient from './api'

class AuthService {
  /**
   * Login with credentials
   */
  async login(email, password) {
    const response = await apiClient.post('/auth/login', {
      email,
      password,
    })
    const result = response.data.data || response.data
    
    if (result.access_token) {
      localStorage.setItem('access_token', result.access_token)
      localStorage.setItem('user', JSON.stringify(result.user))
    }
    
    return result
  }

  /**
   * Register new user
   */
  async register(email, password, name) {
    const response = await apiClient.post('/auth/register', {
      email,
      password,
      name,
    })
    const result = response.data.data || response.data
    
    if (result.access_token) {
      localStorage.setItem('access_token', result.access_token)
      localStorage.setItem('user', JSON.stringify(result.user))
    }
    
    return result
  }

  /**
   * Logout
   */
  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  /**
   * Get current user
   */
  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!localStorage.getItem('access_token')
  }

  /**
   * Get user profile
   */
  async getProfile() {
    const response = await apiClient.get('/users/me')
    return response.data.data
  }

  /**
   * Update user profile
   */
  async updateProfile(updates) {
    const response = await apiClient.put('/users/me', updates)
    const result = response.data.data || response.data
    localStorage.setItem('user', JSON.stringify(result))
    return result
  }
}

export default new AuthService()
