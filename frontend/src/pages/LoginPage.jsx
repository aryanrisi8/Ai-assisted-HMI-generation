/**
 * Login Page
 * 
 * User authentication form
 */

import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { FormInput } from '../components/FormInput'
import Button from '../components/Button'
import Alert from '../components/Alert'

export default function LoginPage() {
  const navigate = useNavigate()
  const { login, error } = useAuth()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })
  const [validationErrors, setValidationErrors] = useState({})

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    if (validationErrors[name]) {
      setValidationErrors((prev) => ({ ...prev, [name]: null }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await login(formData.email, formData.password)
      navigate('/dashboard')
    } catch (err) {
      setValidationErrors({
        submit: err.response?.data?.detail || 'Login failed',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-2 text-center">Welcome Back</h1>
        <p className="text-gray-600 text-center mb-8">
          Sign in to your account to continue
        </p>

        {error && (
          <Alert type="error" message={error} closeable={false} autoClose={0} />
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
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

          <Button
            type="submit"
            loading={loading}
            disabled={loading}
            className="w-full"
          >
            Sign In
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Don't have an account?{' '}
            <Link to="/auth/register" className="text-primary-600 hover:text-primary-700 font-medium">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
