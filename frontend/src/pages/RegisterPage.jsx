/**
 * Register Page
 * 
 * User registration form
 */

import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { FormInput } from '../components/FormInput'
import Button from '../components/Button'
import Alert from '../components/Alert'

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register, error } = useAuth()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  })
  const [validationErrors, setValidationErrors] = useState({})

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: null }))
    }
  }

  const validateForm = () => {
    const errors = {}

    if (!formData.name.trim()) {
      errors.name = 'Name is required'
    }
    if (!formData.email.trim()) {
      errors.email = 'Email is required'
    }
    if (formData.password.length < 8) {
      errors.password = 'Password must be at least 8 characters'
    }
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match'
    }

    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validateForm()) return

    setLoading(true)

    try {
      await register(formData.email, formData.password, formData.name)
      navigate('/dashboard')
    } catch (err) {
      setValidationErrors({
        submit: err.response?.data?.detail || 'Registration failed',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-2 text-center">Create Account</h1>
        <p className="text-gray-600 text-center mb-8">
          Join us to get started with intelligent dashboards
        </p>

        {error && (
          <Alert type="error" message={error} closeable={false} autoClose={0} />
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <FormInput
            label="Full Name"
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="John Doe"
            required
            error={validationErrors.name}
          />

          <FormInput
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="you@example.com"
            required
            error={validationErrors.email}
          />

          <FormInput
            label="Password"
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="••••••••"
            required
            error={validationErrors.password}
          />

          <FormInput
            label="Confirm Password"
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            placeholder="••••••••"
            required
            error={validationErrors.confirmPassword}
          />

          <Button
            type="submit"
            loading={loading}
            disabled={loading}
            className="w-full"
          >
            Create Account
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link to="/auth/login" className="text-primary-600 hover:text-primary-700 font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
