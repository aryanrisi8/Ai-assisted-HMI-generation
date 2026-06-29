# Frontend Architecture

## Overview

The frontend is built with React 18, using Vite for build tooling and Tailwind CSS for styling. It implements a modular architecture with clear separation of concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│          HTML Entry Point               │
│         (index.html)                    │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │   React App     │
        │  (App.jsx)      │
        └────────┬────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
  ┌─▼──────────┐        ┌────▼──────┐
  │AuthProvider│        │RouterProvider
  └─┬──────────┘        └────┬──────┘
    │                        │
    ├──────────────┬─────────┤
    │              │         │
 Pages      Layouts    Components
    │              │         │
    ├─Home         ├─Auth    ├─Nav
    ├─Login        ├─Dashboard├─Sidebar
    ├─Register     │         ├─Alert
    ├─Dashboard    │         ├─Button
    └─Metadata     │         ├─Forms
                   │         └─Spinner
                   │
         ┌─────────▼─────────┐
         │   Services Layer  │
         └────────┬──────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼──┐  ┌───────▼──────┐  ┌──▼────┐
│ API  │  │   Auth       │  │Meta   │
│      │  │   Service    │  │       │
└──────┘  └──────────────┘  └───────┘

         ┌──────────────────┐
         │  Backend API     │
         │  (FastAPI)       │
         └──────────────────┘
```

## Core Concepts

### 1. Routing (React Router v6)

```
/                       → HomePage
/auth/login            → LoginPage
/auth/register         → RegisterPage
/dashboard             → DashboardLayout → DashboardPage
/dashboard/metadata    → DashboardLayout → MetadataPage
*                      → NotFoundPage
```

**Protected Routes**: Routes under `/dashboard` require authentication.

### 2. Authentication Flow

```
User Input (email, password)
    ↓
AuthService.login()
    ↓
API Request → Backend
    ↓
Success → Save token to localStorage
    ↓
AuthContext.setUser()
    ↓
Update UI / Redirect to Dashboard
```

### 3. State Management

**Global State**: `AuthContext`
- User information
- Loading state
- Error messages
- Login/Logout actions

**Local State**: Component-level with `useState`
- Form data
- UI toggles
- Component-specific state

### 4. Data Fetching

```
Component
    ↓
useFetch() Hook
    ↓
Service Layer
    ↓
API Client (Axios)
    ↓
Request Interceptor (Add token)
    ↓
Backend API
```

## Layered Architecture

### 1. Presentation Layer (Components)

Components are organized by:
- **Pages** - Full page components
- **Layouts** - Page layout templates
- **Components** - Reusable UI elements

### 2. State Management Layer

- **Contexts** - Global state (AuthContext)
- **Hooks** - State logic (useAuth, useFetch, useAsync)
- **Local State** - Component state (useState)

### 3. Services Layer

- **API Client** - Axios instance with interceptors
- **Service Classes** - Domain-specific API calls
  - AuthService
  - MetadataService
  - DashboardService

### 4. Infrastructure Layer

- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Router** - Routing

## Data Flow

### Request Flow

```
Component
    ↓
Hook (useFetch, useAuth)
    ↓
Service (authService, metadataService)
    ↓
API Client (apiClient)
    ↓
Request Interceptor
    ├─ Add Authorization header
    └─ Add Config
    ↓
HTTP Request
    ↓
Backend API
```

### Response Flow

```
Backend Response
    ↓
Response Interceptor
    ├─ Handle 401 → Redirect to login
    └─ Pass through or error
    ↓
Service processes data
    ↓
Hook updates state
    ↓
Component re-renders
    ↓
UI Updates
```

## Component Patterns

### Functional Component with Hooks

```javascript
import { useState, useEffect } from 'react'
import { useFetch } from '../hooks/useFetch'

export default function MyComponent() {
  // State
  const [local, setLocal] = useState(null)
  
  // Data fetching
  const { data, loading, error } = useFetch(apiCall, [])
  
  // Render
  if (loading) return <Spinner />
  if (error) return <Alert type="error" message={error.message} />
  
  return <div>{data}</div>
}
```

### Protected Page

```javascript
import { useAuth } from '../hooks/useAuth'
import { Navigate } from 'react-router-dom'

export default function AdminPage() {
  const { user, loading } = useAuth()
  
  if (loading) return <Spinner />
  if (!user) return <Navigate to="/login" />
  
  return <div>Admin content</div>
}
```

### Form Component

```javascript
import { useState } from 'react'
import { FormInput } from '../components/FormInput'
import Button from '../components/Button'

export default function MyForm() {
  const [data, setData] = useState({ email: '', name: '' })
  const [loading, setLoading] = useState(false)
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await apiService.create(data)
      // Success handling
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <form onSubmit={handleSubmit}>
      <FormInput 
        label="Email"
        value={data.email}
        onChange={(e) => setData({ ...data, email: e.target.value })}
      />
      <Button type="submit" loading={loading}>Submit</Button>
    </form>
  )
}
```

## API Integration

### Adding New Service

```javascript
// src/services/newService.js
import apiClient from './api'

class NewService {
  async list() {
    const response = await apiClient.get('/new')
    return response.data
  }
  
  async get(id) {
    const response = await apiClient.get(`/new/${id}`)
    return response.data
  }
  
  async create(data) {
    const response = await apiClient.post('/new', data)
    return response.data
  }
}

export default new NewService()
```

### Using in Component

```javascript
import newService from '../services/newService'
import { useFetch } from '../hooks/useFetch'

export default function MyComponent() {
  const { data, loading, error } = useFetch(
    () => newService.list(),
    []
  )
  
  return <div>{/* ... */}</div>
}
```

## Error Handling

### API Errors

```javascript
try {
  await authService.login(email, password)
} catch (error) {
  // error.response.status - HTTP status
  // error.response.data - Error response body
  // error.message - Error message
}
```

### Interceptor Handling

401 errors automatically redirect to login:
```javascript
// In api.js interceptor
if (error.response?.status === 401) {
  localStorage.removeItem('access_token')
  window.location.href = '/login'
}
```

## Performance Optimization

### Code Splitting

Routes are automatically code-split by React Router.

### Lazy Loading

```javascript
import { lazy } from 'react'

const HeavyComponent = lazy(() => import('./HeavyComponent'))
```

### Memoization

```javascript
import { memo, useMemo } from 'react'

const MemoComponent = memo(MyComponent)

const memoValue = useMemo(() => expensiveCalc(), [deps])
```

## Testing Strategy

### Unit Tests
- Test components in isolation
- Mock API calls
- Test hooks

### Integration Tests
- Test complete flows
- Test authentication
- Test routing

### E2E Tests
- Test with real backend
- Test user flows

## Deployment

### Build Process

```bash
npm run build
```

Creates optimized build in `dist/`:
- Minified JavaScript
- CSS minification
- Image optimization
- Code splitting

### Environment Variables

Production `.env`:
```env
VITE_API_BASE_URL=https://api.example.com/api
VITE_API_TIMEOUT=30000
VITE_APP_ENV=production
```

### Hosting Options

- **Vercel** - Optimized for React/Next.js
- **Netlify** - Simple deployment
- **AWS S3 + CloudFront** - Enterprise-grade
- **Docker** - Container deployment

## Security

### Stored Data

- ✅ Token in localStorage during session
- ❌ Never store password
- ❌ Never store sensitive data

### API Security

- ✅ HTTPS only in production
- ✅ CORS properly configured
- ✅ JWT token validation
- ✅ Secure HttpOnly cookies (future)

### Frontend Security

- ✅ Input validation
- ✅ Output encoding
- ✅ CSRF protection
- ✅ XSS prevention (React)

## Monitoring

### Error Logging

Consider adding:
- Sentry for error tracking
- LogRocket for session replay
- Analytics for usage tracking

## File Structure

```
frontend/
├── node_modules/
├── public/
├── src/
│   ├── components/
│   │   ├── Navigation.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Alert.jsx
│   │   ├── Button.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── FormInput.jsx
│   ├── contexts/
│   │   └── AuthContext.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useFetch.js
│   │   └── useAsync.js
│   ├── layouts/
│   │   ├── AuthLayout.jsx
│   │   └── DashboardLayout.jsx
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── MetadataPage.jsx
│   │   └── NotFoundPage.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── auth.js
│   │   ├── metadata.js
│   │   └── dashboard.js
│   ├── utils/
│   │   ├── errorHandler.js
│   │   ├── storage.js
│   │   └── dateUtils.js
│   ├── App.jsx
│   ├── main.jsx
│   ├── index.css
│   └── router.jsx
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── .eslintrc.json
├── .prettierrc
├── .env.example
├── README.md
├── SETUP.md
└── ARCHITECTURE.md
```

## Key Dependencies

- **react** - UI library
- **react-router-dom** - Client routing
- **axios** - HTTP client
- **tailwindcss** - Utility CSS
- **vite** - Build tool
- **lucide-react** - Icon library

## Next Steps

1. Install dependencies: `npm install`
2. Configure environment: `.env`
3. Start dev server: `npm run dev`
4. Build components and pages
5. Integrate with backend
6. Deploy to production
