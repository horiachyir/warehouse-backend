# Depot Pulse Hub Backend

A Django REST API backend for the Depot Pulse Hub application that manages depot operations, staff check-ins, document management, news updates, and performance metrics.

## Features

- **Authentication System**: JWT-based authentication with custom user model
- **Staff Management**: Check-in/check-out system with real-time tracking
- **Document Management**: Upload, download, and categorize documents
- **News & Updates**: Create and manage news items and videos
- **Performance Analytics**: Dashboard metrics and performance tracking

## Project Structure

```
depot-backend/
├── depot_hub/          # Main project configuration
├── authentication/     # User authentication and management
├── staff/             # Staff check-in/out functionality
├── documents/         # Document management system
├── news/             # News items and videos
├── performance/      # Performance metrics and analytics
├── media/           # Uploaded files
├── static/          # Static files
└── venv/           # Virtual environment
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile

### Staff Management
- `GET /api/staff/checkin-records/` - Get today's check-in records
- `POST /api/staff/checkin/` - Check in employee
- `POST /api/staff/checkout/` - Check out employee
- `GET /api/staff/status/` - Get current staff status

### Documents
- `GET /api/documents/` - List all documents
- `POST /api/documents/` - Upload new document
- `GET /api/documents/{id}/` - Get document details
- `POST /api/documents/{id}/download/` - Download document
- `GET /api/documents/categories/` - Get document categories

### News & Videos
- `GET /api/news/` - List news items
- `POST /api/news/` - Create news item
- `GET /api/news/videos/` - List videos
- `POST /api/news/videos/` - Upload video
- `GET /api/news/videos/featured/` - Get featured videos

### Performance
- `GET /api/performance/dashboard/` - Get dashboard data
- `GET /api/performance/metrics/` - Get performance metrics
- `GET /api/performance/staff-in-depot/` - Get staff currently in depot
- `POST /api/performance/update-location/` - Update user location

## Installation & Setup

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install django djangorestframework django-cors-headers pillow python-decouple djangorestframework-simplejwt
   ```

3. **Configure settings**:
   - Update `depot_hub/settings.py` as needed
   - Set up database configuration
   - Configure CORS settings for frontend integration

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**:
   ```bash
   python manage.py runserver
   ```

## Database Models

### CustomUser
- Extended Django user model with additional fields for employee information

### CheckInRecord
- Tracks staff check-in and check-out times

### Document
- Manages uploaded documents with categorization and metadata

### NewsItem
- News articles and updates with priority levels

### Video
- Video content management for training and information

### PerformanceMetric
- Performance tracking and analytics data

### DashboardData
- Daily dashboard statistics and metrics

## Security Features

- JWT token-based authentication
- CORS configuration for frontend integration
- File upload validation
- User permission controls

## Admin Interface

Access the Django admin at `/admin/` to manage:
- Users and permissions
- All application data
- System configuration

## Testing

The API has been tested with the following endpoints:
- User registration and login ✓
- Dashboard data retrieval ✓  
- Staff location tracking ✓
- Token authentication ✓

## CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)

## Default Credentials

- **Admin User**: admin / admin123
- **Test User**: testuser2 / testpass123

## Development Notes

- Uses SQLite database by default (suitable for development)
- Media files are stored locally in `media/` directory
- Static files are served from `static/` directory
- JWT tokens expire after 1 hour (configurable)

## Frontend Integration

This backend is designed to work with the React frontend located in the parent directory. The API provides all the necessary endpoints to support the frontend features including:

- User authentication and session management
- Real-time staff check-in/out functionality
- Document upload and download
- Performance dashboard data
- News and video content management