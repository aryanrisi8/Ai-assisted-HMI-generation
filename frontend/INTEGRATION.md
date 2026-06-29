# Frontend & Backend Integration Guide

## Project Structure

```
d:\hmi\
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── dashboard/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py
│   │   │   ├── rules_engine.py
│   │   │   ├── components.py
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── dashboard_service.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── metadata.py
│   │   │   └── dashboards.py
│   │   └── ...
│   ├── requirements.txt
│   └── README.md
│
└── frontend/                   # React Frontend
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── services/
    │   ├── layouts/
    │   ├── contexts/
    │   ├── hooks/
    │   ├── utils/
    │   ├── App.jsx
    │   ├── main.jsx
    │   ├── index.css
    │   └── router.jsx
    ├── public/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── README.md
```

## Running Both Services

### Terminal 1: Backend (Port 8000)

```bash
cd d:\hmi\backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env
cp .env.example .env

# Run server
uvicorn app.main:app --reload

# Backend running at: http://localhost:8000
# API at: http://localhost:8000/api
# Docs at: http://localhost:8000/docs
```

### Terminal 2: Frontend (Port 5173)

```bash
cd d:\hmi\frontend

# Install dependencies (first time only)
npm install

# Create .env
cp .env.example .env

# Start dev server
npm run dev

# Frontend running at: http://localhost:5173
```

### Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication

```
POST   /api/auth/login          → Login user
POST   /api/auth/register       → Register user
GET    /api/auth/me             → Get current user
PUT    /api/users/me            → Update profile
```

### Metadata (Industrial Systems)

```
GET    /api/metadata                      → List all systems
GET    /api/metadata/{id}                 → Get system by ID
POST   /api/metadata                      → Create system
PUT    /api/metadata/{id}                 → Update system
DELETE /api/metadata/{id}                 → Delete system
GET    /api/metadata/search?q={query}    → Search systems
```

### Dashboard Generation

```
GET    /api/dashboards                    → List dashboards
POST   /api/dashboards/generate/{id}      → Generate dashboard
GET    /api/dashboards/{id}               → Get dashboard
PUT    /api/dashboards/{id}               → Update dashboard
DELETE /api/dashboards/{id}               → Delete dashboard
GET    /api/dashboards/templates          → Get templates
GET    /api/dashboards/recommendations/{id} → Get recommendations
```

## Frontend Environment Variables

### .env.example → .env

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=30000

# App Configuration
VITE_APP_NAME=HMI Dashboard
VITE_APP_ENV=development
```

### Production .env

```env
VITE_API_BASE_URL=https://api.example.com/api
VITE_API_TIMEOUT=30000
VITE_APP_NAME=HMI Dashboard
VITE_APP_ENV=production
```

## Backend CORS Configuration

The backend must enable CORS for the frontend:

```python
# In app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Dev frontend
        "http://localhost:3000",       # Alternative dev port
        "https://example.com",         # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Authentication Flow

### 1. User Registers

```
User → Frontend → Backend
  (name, email, password)
    ↓
Backend validates
    ↓
Create user in DB
    ↓
Generate JWT token
    ↓
Response: token + user
    ↓
Frontend stores token → localStorage
    ↓
Frontend: AuthContext updates
    ↓
User redirected to dashboard
```

### 2. User Logs In

```
User → Frontend (email, password)
    ↓
POST /api/auth/login
    ↓
Backend verifies credentials
    ↓
Generate JWT token
    ↓
Response: token + user
    ↓
Frontend stores token
    ↓
Redirect to dashboard
```

### 3. API Request with Token

```
Frontend component needs data
    ↓
Call service: metadataService.list()
    ↓
Axios interceptor adds header:
   Authorization: Bearer <token>
    ↓
POST request to backend
    ↓
Backend validates token
    ↓
Request processed
    ↓
Response sent to frontend
    ↓
Component receives data
    ↓
Component re-renders
```

### 4. Token Expiration

```
User makes request
    ↓
Backend returns 401 Unauthorized
    ↓
Response interceptor detects 401
    ↓
Clear localStorage (token + user)
    ↓
Redirect to /login
    ↓
User can log in again
```

## Data Flow: Dashboard Generation

### Flow Diagram

```
Frontend
    ↓
User clicks "Generate Dashboard"
    ↓
Pass system ID to backend
    ↓
POST /api/dashboards/generate/{id}
    ↓
Backend receives ID
    ↓
Load system metadata from DB
    ↓
Create Metadata object
    ↓
Pass to DashboardGenerationService
    ↓
1. Rules Engine - Evaluate system
    ↓
2. Template Manager - Find match
    ↓
3. Component Recommender - Suggest UI
    ↓
4. Layout Generator - Position components
    ↓
5. Schema Builder - Create JSON
    ↓
Return layout schema JSON
    ↓
Frontend receives JSON
    ↓
Store/display dashboard
    ↓
User sees generated dashboard
```

### Implementation Example

#### Backend (routes/dashboards.py)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session

from app.services.dashboard_service import DashboardGenerationService

router = APIRouter(prefix="/api/dashboards", tags=["dashboards"])

@router.post("/generate/{metadata_id}")
async def generate_dashboard(
    metadata_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Generate dashboard from metadata."""
    # Load metadata
    metadata = db.query(IndustrialSystem).filter(
        IndustrialSystem.id == metadata_id,
        IndustrialSystem.user_id == current_user.id,
    ).first()
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Metadata not found")
    
    # Convert to schema
    dashboard_metadata = IndustrialSystemMetadata(...)
    
    # Generate
    service = DashboardGenerationService()
    dashboard_json = service.generate(dashboard_metadata)
    
    return dashboard_json
```

#### Frontend (pages/MetadataPage.jsx)

```javascript
import dashboardService from '../services/dashboard'
import { useAsync } from '../hooks/useAsync'

export default function MetadataPage() {
  const { execute: generateDashboard, loading } = useAsync(
    (id) => dashboardService.generateDashboard(id)
  )
  
  const handleGenerate = async (systemId) => {
    try {
      const dashboard = await generateDashboard(systemId)
      // Display dashboard
    } catch (err) {
      // Show error
    }
  }
  
  return (
    <button onClick={() => handleGenerate(systemId)} loading={loading}>
      Generate Dashboard
    </button>
  )
}
```

## Testing the Integration

### 1. Test Backend API

```bash
# Using curl
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get token from response
# Token format: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. Test in Frontend

**Login**:
```bash
1. Open http://localhost:5173
2. Click "Login"
3. Enter email/password
4. Should redirect to dashboard
5. Check localStorage → access_token should be present
```

**Generate Dashboard**:
```bash
1. Go to Systems page
2. Click "Generate" on a system
3. Should call backend API
4. Should return dashboard JSON
5. Display dashboard data
```

### 3. Debug with DevTools

**Network Tab**:
- Should see requests to `http://localhost:8000/api/*`
- Authorization header with token

**Console Tab**:
- Check for errors
- Log API responses

**Application Tab** → localStorage:
- access_token - JWT token
- user - User object (stringified)

## Troubleshooting

### Frontend Can't Connect to Backend

**Error**: `CORS policy: No 'Access-Control-Allow-Origin'`

**Solution**:
1. Check backend CORS middleware
2. Verify `VITE_API_BASE_URL` in .env
3. Check backend is running on port 8000

### 401 Unauthorized

**Problem**: All API calls return 401

**Solutions**:
1. Check token in localStorage
2. Login again
3. Check token isn't expired
4. Verify backend JWT secret

### ECONNREFUSED

**Error**: `connect ECONNREFUSED 127.0.0.1:8000`

**Solution**:
1. Ensure backend is running
2. Check backend listening on port 8000
3. Verify firewall settings

### Session Lost After Page Refresh

**Issue**: Token in localStorage but still redirected to login

**Solution**:
1. Check AuthContext initialization in App.jsx
2. Verify useEffect loads user from localStorage
3. Check token validity

## Performance Considerations

### Frontend Optimization

- Code splitting by routes
- Lazy component loading
- CSS minification
- JavaScript minification
- Image optimization

### Backend Optimization

- Database indexing on frequently queried fields
- Caching for dashboard templates
- Pagination for list endpoints
- Async processing for heavy computation

### API Response Caching

```javascript
// Frontend
const { data } = useFetch(() => metadataService.list(), [])

// Returns cached data on subsequent calls
// Refetch on component mount/dependency change
```

## Security Checklist

**Backend**:
- [ ] Validate all inputs
- [ ] Authenticate all endpoints (except /auth/register, /auth/login)
- [ ] Authorize user-specific data access
- [ ] Hash passwords (bcrypt)
- [ ] Use HTTPS in production
- [ ] Rate limiting on auth endpoints
- [ ] CSRF protection if needed
- [ ] SQL injection prevention (ORM)

**Frontend**:
- [ ] Validate form inputs
- [ ] Never commit .env file
- [ ] Use HTTPS in production
- [ ] Secure token storage (consider HttpOnly cookies)
- [ ] Content Security Policy headers
- [ ] XSS protection

**Network**:
- [ ] HTTPS/TLS in production
- [ ] CORS properly configured
- [ ] No sensitive data in URLs
- [ ] Secure cookie flags (HttpOnly, Secure, SameSite)

## Deployment

### Production Build

```bash
# Frontend
cd d:\hmi\frontend
npm run build

# Output: dist/ folder (ready for hosting)
```

### Deployment Options

**Option 1: Vercel (Frontend)**
```bash
vercel
# Automatically deploys dist/ to Vercel
# Link backend API in .env
```

**Option 2: Docker Compose**
```yaml
version: '3'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=...
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_BASE_URL=http://backend:8000/api
```

**Option 3: AWS**
- Frontend → CloudFront + S3
- Backend → EC2 or Lambda + RDS

## Monitoring & Logging

### Frontend Logging

```javascript
// Consider adding:
// - Sentry for error tracking
// - LogRocket for session replay
// - Google Analytics for usage

import * as Sentry from "@sentry/react"

Sentry.init({
  dsn: "YOUR_DSN",
  environment: import.meta.env.VITE_APP_ENV,
})
```

### Backend Logging

```python
# Already configured in app/core/logging.py
import logging

logger = logging.getLogger(__name__)
logger.info("Request processed")
logger.error("Error occurred", exc_info=True)
```

## Documentation Links

- Backend Dashboard Engine: `d:\hmi\backend\app\dashboard\README.md`
- Frontend Architecture: `d:\hmi\frontend\ARCHITECTURE.md`
- Frontend Setup: `d:\hmi\frontend\SETUP.md`
- Frontend README: `d:\hmi\frontend\README.md`

## Quick Reference

### Backend Commands

```bash
# Start server
uvicorn app.main:app --reload

# View API docs
http://localhost:8000/docs

# Run tests
pytest

# Database migrations (if needed)
alembic upgrade head
```

### Frontend Commands

```bash
# Start dev server
npm run dev

# Build production
npm run build

# Preview build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

## Next Steps

1. ✅ Run both services (backend + frontend)
2. ✅ Test authentication flow
3. ✅ Generate test data
4. ✅ Test dashboard generation
5. ✅ Verify API integration
6. ✅ Test error handling
7. ✅ Performance profiling
8. ✅ Security audit
9. ✅ Production deployment

## Support

For issues:
1. Check error messages in console
2. Review API documentation (http://localhost:8000/docs)
3. Check browser network tab
4. Check server logs
5. Review documentation
6. Contact development team
