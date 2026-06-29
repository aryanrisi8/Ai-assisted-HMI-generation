/**
 * Main App Component
 * 
 * Root component with providers and routing
 */

import { RouterProvider } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { router } from './router'
import './index.css'

export default function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  )
}
