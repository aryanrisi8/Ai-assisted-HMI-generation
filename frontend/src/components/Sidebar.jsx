/**
 * Sidebar Component
 * 
 * Navigation sidebar with:
 * - Menu items
 * - Active state
 * - Collapsible
 */

import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, Database, Settings, ChevronRight } from 'lucide-react'

const menuItems = [
  {
    label: 'Dashboard',
    path: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    label: 'Systems',
    path: '/dashboard/metadata',
    icon: Database,
  },
  {
    label: 'Editor',
    path: '/dashboard/editor',
    icon: LayoutDashboard,
  },
  {
    label: 'Settings',
    path: '/dashboard/settings',
    icon: Settings,
  },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <aside className="w-64 bg-gray-900 text-white shadow-lg">
      <div className="p-6">
        <h2 className="text-xl font-bold text-primary-400">Navigation</h2>
      </div>

      <nav className="space-y-2 px-4">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
              {isActive && <ChevronRight className="w-4 h-4 ml-auto" />}
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="absolute bottom-0 w-64 border-t border-gray-700 p-4">
        <p className="text-xs text-gray-400">
          © 2024 HMI Dashboard. All rights reserved.
        </p>
      </div>
    </aside>
  )
}
