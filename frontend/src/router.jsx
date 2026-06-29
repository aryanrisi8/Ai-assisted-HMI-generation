/**
 * Router Configuration
 * 
 * Application routes with:
 * - Protected routes
 * - Public routes
 * - Route guards
 */

import { createBrowserRouter, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'

import DashboardLayout from './layouts/DashboardLayout'
import AuthLayout from './layouts/AuthLayout'

import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import DashboardEditorPage from './pages/DashboardEditorPage'
import MetadataPage from './pages/MetadataPage'
import NotFoundPage from './pages/NotFoundPage'

/**
 * Protected Route Component
 */
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

/**
 * Router instance
 */
export const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      {
        path: 'login',
        element: <LoginPage />,
      },
      {
        path: 'register',
        element: <RegisterPage />,
      },
    ],
  },
  {
    path: '/dashboard',
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: 'editor',
        element: <DashboardEditorPage />,
      },
      {
        path: 'editor/:dashboardId',
        element: <DashboardEditorPage />,
      },
      {
        path: 'metadata',
        element: <MetadataPage />,
      },
    ],
  },
  {
    path: '*',
    element: <NotFoundPage />,
  },
])
