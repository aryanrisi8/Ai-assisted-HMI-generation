/**
 * Dashboard Layout
 * 
 * Main layout for dashboard pages with sidebar and navigation
 */

import { Outlet } from 'react-router-dom'
import Navigation from '../components/Navigation'
import Sidebar from '../components/Sidebar'

export default function DashboardLayout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
