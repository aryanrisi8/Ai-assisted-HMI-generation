/**
 * Not Found Page (404)
 */

import { Link } from 'react-router-dom'
import Navigation from '../components/Navigation'

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      <Navigation />
      <div className="flex flex-col items-center justify-center py-20 px-4">
        <div className="text-center">
          <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
          <h2 className="text-3xl font-semibold text-gray-700 mb-4">Page Not Found</h2>
          <p className="text-gray-600 mb-8">
            The page you are looking for does not exist.
          </p>
          <Link
            to="/"
            className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700 transition"
          >
            Go Home
          </Link>
        </div>
      </div>
    </div>
  )
}
