/**
 * Auth Layout
 * 
 * Layout for login/register pages
 */

import { Outlet } from 'react-router-dom'
import Navigation from '../components/Navigation'

export default function AuthLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      <Navigation />
      <div className="flex items-center justify-center py-12 px-4">
        <div className="w-full max-w-md">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
