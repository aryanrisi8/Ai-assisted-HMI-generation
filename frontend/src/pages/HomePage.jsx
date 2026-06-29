/**
 * Home Page
 * 
 * Landing page for unauthenticated users
 */

import { Link } from 'react-router-dom'
import { ArrowRight, Zap, BarChart3, Lock } from 'lucide-react'
import Navigation from '../components/Navigation'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100">
      <Navigation />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          Industrial HMI Dashboard
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Real-time monitoring and control of industrial systems with intelligent dashboards generated from your infrastructure metadata.
        </p>
        <div className="flex flex-col md:flex-row gap-4 justify-center">
          <Link
            to="/auth/login"
            className="bg-primary-600 text-white px-8 py-3 rounded-lg hover:bg-primary-700 transition inline-flex items-center space-x-2"
          >
            <span>Get Started</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/auth/register"
            className="border-2 border-primary-600 text-primary-600 px-8 py-3 rounded-lg hover:bg-primary-50 transition"
          >
            Create Account
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-16">Key Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="p-6 rounded-lg border border-gray-200 hover:shadow-lg transition">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Intelligent Generation</h3>
              <p className="text-gray-600">
                Automatically generate optimized dashboards based on your industrial system metadata and signals.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="p-6 rounded-lg border border-gray-200 hover:shadow-lg transition">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="w-6 h-6 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Real-Time Monitoring</h3>
              <p className="text-gray-600">
                Monitor multiple sensors and signals in real-time with customizable visualizations.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="p-6 rounded-lg border border-gray-200 hover:shadow-lg transition">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <Lock className="w-6 h-6 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Secure & Reliable</h3>
              <p className="text-gray-600">
                Enterprise-grade security with role-based access control and data encryption.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p>&copy; 2024 HMI Dashboard. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
