"""
Pytest configuration and shared fixtures for all tests.

This module provides common test setup, database configuration,
and shared fixtures used across all test modules.
"""

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from src.api.main import app
from src.core.database import get_db, Base
from src.models.user import User
from src.models.task import Task
from src.repositories.user_repository import UserRepository
from src.repositories.task_repository import TaskRepository
from src.services.authentication.password_service import password_service
from src.services.authentication.jwt_service import jwt_service
from src.services.authentication.auth_service import AuthenticationService
from src.services.task_management.task_service import TaskService


# Test database configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", 
    "sqlite:///./test_coverage.db"
)

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {},
    poolclass=StaticPool if "sqlite" in TEST_DATABASE_URL else None,
    echo=False
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def setup_database():
    """Set up test database for the entire test session."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up after all tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Create database session for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def user_repository():
    """Create user repository instance."""
    return UserRepository()


@pytest.fixture
def task_repository():
    """Create task repository instance."""
    return TaskRepository()


@pytest.fixture
def auth_service():
    """Create authentication service instance."""
    return AuthenticationService()


@pytest.fixture
def task_service():
    """Create task service instance."""
    return TaskService()


@pytest.fixture
def sample_user_id(db_session, user_repository):
    """Create a sample user for testing."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "hashed_password": password_service.hash_password("Test@123"),
        "full_name": "Test User",
        "is_active": True,
        "is_verified": True
    }
    user = user_repository.create_user(db_session, user_data)
    return user.id


@pytest.fixture
def sample_user_token(sample_user_id, jwt_service):
    """Create a JWT token for the sample user."""
    return jwt_service.create_access_token(
        data={"sub": str(sample_user_id), "email": "test@example.com"}
    )


@pytest.fixture
def sample_task_id(db_session, task_repository, sample_user_id):
    """Create a sample task for testing."""
    task_data = {
        "title": "Test Task",
        "description": "Test description",
        "status": "TODO",
        "owner_id": sample_user_id
    }
    task = task_repository.create_task(db_session, task_data)
    return task.id
