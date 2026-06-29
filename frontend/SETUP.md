# Frontend Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Configuration

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your backend URL:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=30000
VITE_APP_ENV=development
```

### 3. Start Development Server

```bash
npm run dev
```

Frontend runs at: `http://localhost:5173`

## Project Structure

```
src/
├── components/          # UI components
├── pages/              # Page components
├── layouts/            # Layout components
├── services/           # API clients
├── contexts/           # React Context
├── hooks/              # Custom hooks
├── utils/              # Utilities
├── App.jsx             # Root component
├── main.jsx            # Entry point
├── index.css           # Global styles
└── router.jsx          # Routes
```

## Services Layer

All API calls go through the services layer:

- `services/api.js` - Axios instance with interceptors
- `services/auth.js` - Authentication API calls
- `services/metadata.js` - Industrial systems API
- `services/dashboard.js` - Dashboard API

## Authentication Flow

1. **Login/Register** → `AuthService`
2. **Store Token** → localStorage
3. **Add to Requests** → Axios interceptor
4. **Update Context** → `AuthContext`
5. **Protect Routes** → `ProtectedRoute`

## State Management

Using React Context for:
- **AuthContext** - User authentication state
- No Redux/Zustand needed (simple architecture)

Add more contexts as needed:
```javascript
// src/contexts/ThemeContext.jsx
// src/contexts/NotificationContext.jsx
```

## Custom Hooks

### useAuth
```javascript
const { user, loading, error, login, logout, register, isAuthenticated } = useAuth()
```

### useFetch
```javascript
const { data, loading, error, retry } = useFetch(() => apiCall())
```

### useAsync
```javascript
const { execute, loading, error, data } = useAsync(asyncFn)
```

## Component Patterns

### Functional Component with Hooks
```javascript
import { useState } from 'react'
import { useFetch } from '../hooks/useFetch'

export default function MyComponent() {
  const [state, setState] = useState(null)
  const { data, loading, error } = useFetch(fetchFn)

  return <div>...</div>
}
```

### Using API Services
```javascript
import metadataService from '../services/metadata'

const data = await metadataService.getMetadata(id)
```

### Protected Page
```javascript
import { useAuth } from '../hooks/useAuth'

export default function AdminPage() {
  const { user } = useAuth()

  if (!user) return <Navigate to="/login" />

  return <div>Admin content</div>
}
```

## Styling

### Tailwind Classes
```html
<!-- Utility-first approach -->
<div className="flex items-center justify-center p-4 bg-primary-600 text-white rounded-lg">
  Content
</div>
```

### Custom Colors
Available in `tailwind.config.js`:
- primary (500, 600, 700, 900)
- danger (500, 600, 700)
- success (500, 600, 700)
- warning (500, 600, 700)

### Responsive Design
```html
<!-- Mobile first -->
<div className="w-full md:w-1/2 lg:w-1/3">
  Responsive content
</div>
```

## Building for Production

```bash
npm run build
```

Output: `dist/` directory

### Preview Build
```bash
npm run preview
```

## Deployment Options

### Option 1: Vercel
```bash
npm install -g vercel
vercel
```

### Option 2: Netlify
```bash
npm run build
# Upload dist/ folder
```

### Option 3: Docker
```bash
docker build -t hmi-frontend .
docker run -p 80:80 hmi-frontend
```

## API Integration Checklist

- [ ] Backend running at `VITE_API_BASE_URL`
- [ ] CORS enabled on backend
- [ ] Auth endpoints working (/auth/login, /auth/register)
- [ ] Token-based auth working
- [ ] Metadata endpoints available
- [ ] Dashboard endpoints available

## Common Issues

### CORS Error
**Issue**: `No 'Access-Control-Allow-Origin' header`
**Solution**: Enable CORS on backend

### API 401 Errors
**Issue**: Unauthorized requests
**Solution**: Check token in localStorage

### Blank Page
**Issue**: React not rendering
**Solution**: Check browser console for errors

### API Calls Not Working
**Issue**: 404 errors
**Solution**: Check `VITE_API_BASE_URL` in .env

## Development Workflow

1. **Create new page** in `src/pages/`
2. **Create components** in `src/components/`
3. **Add routes** in `src/router.jsx`
4. **Call APIs** via services
5. **Style** with Tailwind classes
6. **Test** locally at `http://localhost:5173`

## Code Style

- **ESLint** - Code linting
- **Prettier** - Code formatting

```bash
npm run lint
npm run format
```

## Performance Tips

- ✅ Use React.memo for expensive components
- ✅ Use useMemo for expensive calculations
- ✅ Lazy load routes with React.lazy()
- ✅ Optimize images
- ✅ Use code splitting
- ✅ Monitor bundle size

## Security

- ✅ Never commit `.env` (in .gitignore)
- ✅ Use HTTPS in production
- ✅ Validate inputs on frontend
- ✅ Don't store sensitive data in localStorage
- ✅ Use secure cookies for tokens (if available)

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure environment variables
3. ✅ Start development server
4. ✅ Verify backend connection
5. ✅ Test authentication flow
6. ✅ Build pages
7. ✅ Deploy to production

## Resources

- [React Docs](https://react.dev)
- [React Router Docs](https://reactrouter.com)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [Axios Docs](https://axios-http.com)
- [Vite Docs](https://vitejs.dev)

## Support

For issues:
1. Check this guide
2. Review console errors
3. Check backend logs
4. Verify API configuration
5. Contact development team
