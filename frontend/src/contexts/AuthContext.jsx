/**
 * Auth Context
 * 
 * Global authentication state management:
 * - Current user
 * - Loading state
 * - Login/logout actions
 */

import { createContext, useState, useEffect, useCallback } from 'react'
import authService from '../services/auth'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Initialize auth state from localStorage
  useEffect(() => {
    const storedUser = authService.getCurrentUser()
    if (storedUser && authService.isAuthenticated()) {
      setUser(storedUser)
    }
    setLoading(false)
  }, [])

  const login = useCallback(async (email, password) => {
    setLoading(true)
    setError(null)
    try {
      const response = await authService.login(email, password)
      setUser(response.user)
      return response
    } catch (err) {
      setError(err.message || 'Login failed')
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    authService.logout()
    setUser(null)
    setError(null)
  }, [])

  const register = useCallback(async (email, password, name) => {
    setLoading(true)
    setError(null)
    try {
      const response = await authService.register(email, password, name)
      setUser(response.user)
      return response
    } catch (err) {
      setError(err.message || 'Registration failed')
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const clearError = useCallback(() => setError(null), [])

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    register,
    clearError,
    isAuthenticated: !!user,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
