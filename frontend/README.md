# HMI Dashboard Frontend

React-based frontend for Industrial HMI Dashboard with real-time monitoring and control.

## Features

- **Modern React** - Latest React 18 with hooks and Suspense
- **React Router** - Client-side routing with protected routes
- **Axios** - HTTP client with interceptors and error handling
- **Tailwind CSS** - Utility-first CSS framework
- **Authentication** - JWT-based auth with context
- **Form Handling** - Reusable form components with validation
- **State Management** - React Context for global state
- **Custom Hooks** - `useAuth`, `useFetch`, `useAsync`

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navigation.jsx
│   ├── Sidebar.jsx
│   ├── Alert.jsx
│   ├── Button.jsx
│   ├── LoadingSpinner.jsx
│   ├── FormInput.jsx
│   └── ...
├── pages/              # Page components
│   ├── HomePage.jsx
│   ├── LoginPage.jsx
│   ├── RegisterPage.jsx
│   ├── DashboardPage.jsx
│   ├── MetadataPage.jsx
│   └── NotFoundPage.jsx
├── layouts/            # Layout components
│   ├── AuthLayout.jsx
│   └── DashboardLayout.jsx
├── services/           # API integration
│   ├── api.js          # Axios instance
│   ├── auth.js         # Auth endpoints
│   ├── metadata.js     # Metadata endpoints
│   └── dashboard.js    # Dashboard endpoints
├── contexts/           # React Context
│   └── AuthContext.jsx
├── hooks/              # Custom hooks
│   ├── useAuth.js
│   ├── useFetch.js
│   └── useAsync.js
├── utils/              # Utilities
├── App.jsx             # Root component
├── main.jsx            # Entry point
├── index.css           # Global styles
└── router.jsx          # Route configuration
```

## Installation

```bash
# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev

# Build for production
npm run build
```

## Environment Variables

```bash
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=30000
VITE_APP_NAME=HMI Dashboard
VITE_APP_ENV=development
```

## API Integration

### Authentication Service

```javascript
import authService from './services/auth'

// Login
await authService.login(email, password)

// Register
await authService.register(email, password, name)

// Logout
authService.logout()

// Check auth
if (authService.isAuthenticated()) { ... }

// Get current user
const user = authService.getCurrentUser()
```

### Metadata Service

```javascript
import metadataService from './services/metadata'

// List systems
await metadataService.listMetadata(offset, limit)

// Get system
await metadataService.getMetadata(id)

// Create system
await metadataService.createMetadata(data)

// Update system
await metadataService.updateMetadata(id, data)

// Delete system
await metadataService.deleteMetadata(id)

// Search
await metadataService.searchMetadata(query)
```

### Dashboard Service

```javascript
import dashboardService from './services/dashboard'

// Generate dashboard
await dashboardService.generateDashboard(metadataId)

// Get templates
await dashboardService.getTemplates()

// Get recommendations
await dashboardService.getRecommendations(metadataId)

// Save dashboard
await dashboardService.saveDashboard(name, layout, metadataId)

// Get dashboard
await dashboardService.getDashboard(id)

// List dashboards
await dashboardService.listDashboards(offset, limit)

// Delete dashboard
await dashboardService.deleteDashboard(id)

// Update dashboard
await dashboardService.updateDashboard(id, updates)
```

## Custom Hooks

### useAuth

```javascript
import { useAuth } from './hooks/useAuth'

const { user, loading, error, login, logout, register, isAuthenticated } = useAuth()
```

### useFetch

```javascript
import { useFetch } from './hooks/useFetch'

const { data, loading, error, retry } = useFetch(fetchFn, dependencies)
```

### useAsync

```javascript
import { useAsync } from './hooks/useAsync'

const { execute, loading, error, data } = useAsync(asyncFn)
```

## Routing

### Protected Routes

Routes under `/dashboard` are protected and require authentication.

```javascript
// Public routes
GET  /
GET  /auth/login
GET  /auth/register

// Protected routes
GET  /dashboard
GET  /dashboard/metadata
GET  /dashboard/settings
```

### Route Guards

The `ProtectedRoute` component in `router.jsx` automatically handles:
- Redirecting unauthenticated users to login
- Showing loading spinner while checking auth
- Rendering protected content if authenticated

## Components

### Navigation

Main navigation bar with:
- Logo and branding
- Navigation links
- User menu with logout
- Responsive design

### Sidebar

Dashboard sidebar with:
- Menu items
- Active state indication
- Icons
- Collapsible support

### Button

Reusable button with variants:
- `primary` - Primary action
- `secondary` - Secondary action
- `danger` - Destructive action
- `outline` - Outlined style

Sizes: `sm`, `md`, `lg`

### Form Components

- `FormInput` - Text input with validation
- `FormTextarea` - Textarea with validation
- `FormSelect` - Select dropdown with validation

### Alert

Component for displaying messages:
- Types: `error`, `success`, `warning`, `info`
- Auto-close support
- Closeable option

### LoadingSpinner

Animated loading indicator with sizes: `sm`, `md`, `lg`

## Styling

### Tailwind CSS

Custom color scheme:
```javascript
colors: {
  primary: { 50, 100, 500, 600, 700, 900 },
  danger: { 500, 600, 700 },
  success: { 500, 600, 700 },
  warning: { 500, 600, 700 },
}
```

### Dark Mode

Built-in support for dark mode via Tailwind's `dark:` prefix.

## API Interceptors

### Request Interceptor

Automatically adds JWT token to requests:
```javascript
Authorization: Bearer <token>
```

### Response Interceptor

Handles:
- 401 Unauthorized: Redirects to login
- Other errors: Passes to handler

## Development

```bash
# Run development server
npm run dev

# Build production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

## Production Build

```bash
npm run build
```

Output is in `dist/` directory.

## Browser Support

- Chrome/Edge latest
- Firefox latest
- Safari latest

## Performance

- Code splitting with React Router
- Lazy loading of components
- Optimized bundle size (~200KB gzipped)
- CSS minification

## Security

- HTTPS recommended in production
- JWT token stored in localStorage
- CORS configured on backend
- XSS protection via React
- CSRF tokens if needed

## Deployment

### Vercel

```bash
npm install -g vercel
vercel
```

### Netlify

```bash
npm run build
# Deploy dist/ folder
```

### Docker

```dockerfile
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Troubleshooting

### CORS Issues

Ensure backend is configured for CORS:
```python
# FastAPI
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection

Check `.env` file `VITE_API_BASE_URL` matches backend URL.

### Authentication Issues

Check localStorage for `access_token` in browser DevTools.

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

Proprietary - All rights reserved

## Support

For issues or questions, contact the development team.
