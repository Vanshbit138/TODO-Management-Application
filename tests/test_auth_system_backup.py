"""
Authentication system tests.

This module contains comprehensive tests for the authentication system including
user registration, login, token validation, and security features.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.api.main import app
from src.core.database import get_db, Base
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.services.authentication.password_service import password_service
from src.services.authentication.jwt_service import jwt_service


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def setup_database():
    """Set up test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def db_session():
    """Create database session for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def user_repository():
    """Create user repository for testing."""
    return UserRepository()


class TestPasswordService:
    """Test password service functionality."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword123!"
        hashed = password_service.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert password_service.verify_password(password, hashed)
    
    def test_verify_password(self):
        """Test password verification."""
        password = "TestPassword123!"
        hashed = password_service.hash_password(password)
        
        assert password_service.verify_password(password, hashed)
        assert not password_service.verify_password("wrong_password", hashed)
        assert not password_service.verify_password("", hashed)
        assert not password_service.verify_password(password, "")
    
    def test_password_strength_validation(self):
        """Test password strength validation."""
        # Valid password
        valid_password = "TestPassword123!"
        is_valid, error = password_service.validate_password_strength(valid_password)
        assert is_valid
        assert error is None
        
        # Too short
        short_password = "Test1!"
        is_valid, error = password_service.validate_password_strength(short_password)
        assert not is_valid
        assert "at least 8 characters" in error
        
        # No uppercase
        no_upper = "testpassword123!"
        is_valid, error = password_service.validate_password_strength(no_upper)
        assert not is_valid
        assert "uppercase letter" in error
        
        # No lowercase
        no_lower = "TESTPASSWORD123!"
        is_valid, error = password_service.validate_password_strength(no_lower)
        assert not is_valid
        assert "lowercase letter" in error
        
        # No digit
        no_digit = "TestPassword!"
        is_valid, error = password_service.validate_password_strength(no_digit)
        assert not is_valid
        assert "digit" in error
        
        # No special character
        no_special = "TestPassword123"
        is_valid, error = password_service.validate_password_strength(no_special)
        assert not is_valid
        assert "special character" in error


class TestJWTService:
    """Test JWT service functionality."""
    
    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data)
        
        assert token is not None
        assert len(token) > 0
    
    def test_verify_token(self):
        """Test JWT token verification."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data)
        
        payload = jwt_service.verify_token(token)
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"
    
    def test_get_user_id_from_token(self):
        """Test extracting user ID from token."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data)
        
        user_id = jwt_service.get_user_id_from_token(token)
        assert user_id == 123
    
    def test_get_user_email_from_token(self):
        """Test extracting user email from token."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data)
        
        email = jwt_service.get_user_email_from_token(token)
        assert email == "test@example.com"


class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_register_user_success(self, client, setup_database):
        """Test successful user registration."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["full_name"] == user_data["full_name"]
        assert data["is_active"] is True
        assert data["is_verified"] is False
        assert "id" in data
    
    def test_register_user_duplicate_email(self, client, setup_database):
        """Test registration with duplicate email."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        
        # Register first user
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Try to register with same email
        user_data["username"] = "testuser2"
        response2 = client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "Email already registered" in response2.json()["detail"]
    
    def test_register_user_duplicate_username(self, client, setup_database):
        """Test registration with duplicate username."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        
        # Register first user
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Try to register with same username
        user_data["email"] = "test2@example.com"
        response2 = client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400
        assert "Username already taken" in response2.json()["detail"]
    
    def test_register_user_weak_password(self, client, setup_database):
        """Test registration with weak password."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "weak",
            "full_name": "Test User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error


class TestUserLogin:
    """Test user login functionality."""
    
    def test_login_success(self, client, setup_database):
        """Test successful user login."""
        # Register user first
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Login
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == user_data["email"]
    
    def test_login_wrong_password(self, client, setup_database):
        """Test login with wrong password."""
        # Register user first
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Login with wrong password
        login_data = {
            "email": "test@example.com",
            "password": "WrongPassword123!"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client, setup_database):
        """Test login with nonexistent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "TestPassword123!"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]


class TestProtectedEndpoints:
    """Test protected endpoints requiring authentication."""
    
    def test_get_current_user_success(self, client, setup_database):
        """Test getting current user with valid token."""
        # Register and login user
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
    
    def test_get_current_user_invalid_token(self, client, setup_database):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
    
    def test_get_current_user_no_token(self, client, setup_database):
        """Test getting current user without token."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 403
        assert "Not authenticated" in response.json()["detail"]


class TestTokenRefresh:
    """Test token refresh functionality."""
    
    def test_refresh_token_success(self, client, setup_database):
        """Test successful token refresh."""
        # Register and login user
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        token = login_response.json()["access_token"]
        
        # Refresh token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/api/v1/auth/refresh", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == user_data["email"]
    
    def test_refresh_token_invalid(self, client, setup_database):
        """Test token refresh with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/api/v1/auth/refresh", headers=headers)
        
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]
