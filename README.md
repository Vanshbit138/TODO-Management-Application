# TODO Management Application - Backend API

A comprehensive TODO management application built with FastAPI, featuring user authentication, task management, and a clean architecture following SOLID principles.

## 🚀 Features

### Authentication System
- **User Registration**: Secure user registration with email validation and password strength requirements
- **JWT Authentication**: Token-based authentication with configurable expiration
- **Password Security**: Bcrypt hashing with strength validation
- **Protected Routes**: Authentication dependencies for secure endpoints

### Task Management
- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Task Status Tracking**: TODO, IN_PROGRESS, COMPLETED statuses
- **User Ownership**: Tasks are scoped to authenticated users
- **Due Date Support**: Optional due date tracking for tasks

### Database & Architecture
- **SQLAlchemy ORM**: Modern async-compatible ORM
- **Alembic Migrations**: Database schema versioning
- **Clean Architecture**: Repository pattern with service layer
- **Dependency Injection**: FastAPI dependency system

## 🛠️ Tech Stack

- **FastAPI** (Python 3.12+) - Modern, fast web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Alembic** - Database migration tool
- **PostgreSQL/SQLite** - Database (configurable)
- **JWT (PyJWT)** - JSON Web Token authentication
- **Pydantic** - Data validation and settings management
- **pytest** - Testing framework with coverage

## 📁 Project Structure

```
src/
├── api/
│   ├── main.py                    # FastAPI app entrypoint
│   └── routers/                   # API routes
│       ├── auth.py                # Authentication endpoints
│       └── tasks.py               # Task management endpoints
├── core/
│   ├── config.py                  # Configuration management
│   ├── database.py                # Database connection & session
│   ├── dependencies.py            # FastAPI dependencies
│   └── interfaces.py              # Shared interfaces
├── models/
│   ├── user.py                    # User SQLAlchemy model
│   └── task.py                    # Task SQLAlchemy model
├── repositories/
│   ├── user_repository.py         # User data access
│   └── task_repository.py         # Task data access
├── services/
│   ├── authentication/           # Auth business logic
│   │   ├── auth_service.py        # Authentication service
│   │   ├── password_service.py    # Password hashing
│   │   └── jwt_service.py         # JWT token management
│   └── task_management/           # Task business logic
├── schemas/
│   └── auth.py                    # Pydantic schemas for auth
└── tests/
    ├── test_auth_system.py        # Authentication tests
    ├── test_task_endpoints.py     # Task integration tests
    └── test_task_simple.py        # Task unit tests
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip (Python package manager)
- PostgreSQL (optional, SQLite supported for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd TODO-Management-Application
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements/requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your database URL and secret key
   ```

5. **Run database migrations**
   ```bash
   python3 -m alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

```env
# Database Configuration
DATABASE_URL=sqlite:///./todo_management.db  # or PostgreSQL URL

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=True
ENVIRONMENT=development
API_V1_STR=/api/v1

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Database Setup

#### SQLite (Development)
```bash
# Already configured in .env
DATABASE_URL=sqlite:///./todo_management.db
```

#### PostgreSQL (Production)
```bash
# Install PostgreSQL and create database
createdb todo_management_db

# Update .env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_management_db
```

## 📚 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login user | No |
| GET | `/api/v1/auth/me` | Get current user info | Yes |
| POST | `/api/v1/auth/refresh` | Refresh access token | Yes |

### Task Endpoints (Coming Soon)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/tasks/` | Get user's tasks | Yes |
| POST | `/api/v1/tasks/` | Create new task | Yes |
| GET | `/api/v1/tasks/{id}` | Get specific task | Yes |
| PUT | `/api/v1/tasks/{id}` | Update task | Yes |
| DELETE | `/api/v1/tasks/{id}` | Delete task | Yes |

## 🔐 Authentication

### Registration
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "TestPassword123!",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "TestPassword123!"
  }'
```

### Using Access Token
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_auth_system.py -v
```

### Test Coverage
```bash
# Generate coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## 🗄️ Database Migrations

### Create Migration
```bash
python3 -m alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
python3 -m alembic upgrade head
```

### Rollback Migration
```bash
python3 -m alembic downgrade -1
```

## 🏗️ Development

### Code Quality
- **Type Hints**: All functions use Python type hints
- **Docstrings**: Google-style docstrings on all public members
- **SOLID Principles**: Clean architecture with separation of concerns
- **Error Handling**: Comprehensive HTTP exception handling

### Adding New Features

1. **Models**: Add SQLAlchemy models in `src/models/`
2. **Schemas**: Add Pydantic schemas in `src/schemas/`
3. **Repository**: Add data access methods in `src/repositories/`
4. **Service**: Add business logic in `src/services/`
5. **Router**: Add API endpoints in `src/api/routers/`
6. **Tests**: Add comprehensive tests in `tests/`

## 🚀 Deployment

### Production Checklist

- [ ] Update `SECRET_KEY` with strong random value
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up proper CORS origins
- [ ] Configure logging
- [ ] Set up monitoring and health checks

### Docker Support (Coming Soon)
```bash
# Build and run with Docker
docker build -t todo-api .
docker run -p 8000:8000 todo-api
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the test files for usage examples

---

**Happy coding! 🎉**
