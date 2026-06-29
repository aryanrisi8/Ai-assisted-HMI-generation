/**
 * Navigation Component
 * 
 * Top navigation bar with:
 * - Branding
 * - Navigation links
 * - User menu
 * - Authentication state
 */

import { Link, useNavigate } from 'react-router-dom'
import { Menu, LogOut, Settings, User } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { useState } from 'react'

export default function Navigation() {
  const { user, logout, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">H</span>
            </div>
            <span className="text-xl font-bold text-gray-900">
              HMI Dashboard
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            {isAuthenticated && (
              <>
                <Link
                  to="/dashboard"
                  className="text-gray-700 hover:text-primary-600 transition"
                >
                  Dashboard
                </Link>
                <Link
                  to="/dashboard/metadata"
                  className="text-gray-700 hover:text-primary-600 transition"
                >
                  Systems
                </Link>
              </>
            )}
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setMenuOpen(!menuOpen)}
                  className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition"
                >
                  <User className="w-5 h-5 text-gray-700" />
                  <span className="text-gray-700 text-sm">{user?.name || user?.email}</span>
                </button>

                {/* Dropdown Menu */}
                {menuOpen && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg z-50">
                    <Link
                      to="/profile"
                      className="flex items-center space-x-2 px-4 py-3 hover:bg-gray-50 text-gray-700"
                      onClick={() => setMenuOpen(false)}
                    >
                      <Settings className="w-4 h-4" />
                      <span>Settings</span>
                    </Link>
                    <button
                      onClick={() => {
                        handleLogout()
                        setMenuOpen(false)
                      }}
                      className="flex items-center space-x-2 w-full px-4 py-3 hover:bg-gray-50 text-red-600 border-t"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link
                  to="/auth/login"
                  className="text-gray-700 hover:text-primary-600 transition"
                >
                  Login
                </Link>
                <Link
                  to="/auth/register"
                  className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>

          {/* Mobile Menu */}
          <button className="md:hidden text-gray-700">
            <Menu className="w-6 h-6" />
          </button>
        </div>
      </div>
    </nav>
  )
}
