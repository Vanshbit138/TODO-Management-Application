"""
Improved Authentication system tests with comprehensive coverage.

This module contains comprehensive tests for the authentication system including
user registration, login, token validation, and security features.
"""

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from src.schemas.auth import UserRegistration, UserLogin, TokenResponse, UserResponse
from src.services.authentication.password_service import password_service
from src.services.authentication.jwt_service import jwt_service


class TestUserRegistration:
    """Test user registration functionality."""

    def test_register_user_success(self, client, db_session, setup_database):
        """Test successful user registration."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "NewUser@123",
            "full_name": "New User"
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

    def test_register_user_duplicate_email(self, client, db_session, setup_database, sample_user_id):
        """Test registration with duplicate email."""
        user_data = {
            "email": "test@example.com",  # Same as sample user
            "username": "differentuser",
            "password": "Different@123",
            "full_name": "Different User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_user_duplicate_username(self, client, db_session, setup_database, sample_user_id):
        """Test registration with duplicate username."""
        user_data = {
            "email": "different@example.com",
            "username": "testuser",  # Same as sample user
            "password": "Different@123",
            "full_name": "Different User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_register_user_invalid_email(self, client, db_session, setup_database):
        """Test registration with invalid email format."""
        user_data = {
            "email": "invalid-email",
            "username": "validuser",
            "password": "Valid@123",
            "full_name": "Valid User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422

    def test_register_user_weak_password(self, client, db_session, setup_database):
        """Test registration with weak password."""
        user_data = {
            "email": "weak@example.com",
            "username": "weakuser",
            "password": "123",  # Too weak
            "full_name": "Weak User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422

    def test_register_user_short_username(self, client, db_session, setup_database):
        """Test registration with short username."""
        user_data = {
            "email": "short@example.com",
            "username": "ab",  # Too short
            "password": "Valid@123",
            "full_name": "Short User"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422


class TestUserLogin:
    """Test user login functionality."""

    def test_login_success(self, client, db_session, setup_database, sample_user_id):
        """Test successful user login."""
        login_data = {
            "email": "test@example.com",
            "password": "Test@123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == login_data["email"]

    def test_login_wrong_password(self, client, db_session, setup_database, sample_user_id):
        """Test login with wrong password."""
        login_data = {
            "email": "test@example.com",
            "password": "WrongPassword@123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code in [401, 403]
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_nonexistent_user(self, client, db_session, setup_database):
        """Test login with non-existent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "SomePassword@123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code in [401, 403]
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_invalid_email_format(self, client, db_session, setup_database):
        """Test login with invalid email format."""
        login_data = {
            "email": "invalid-email",
            "password": "SomePassword@123"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 422


class TestProtectedEndpoints:
    """Test protected endpoints that require authentication."""

    def test_get_current_user_success(self, client, db_session, setup_database, sample_user_token):
        """Test getting current user with valid token."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    def test_get_current_user_invalid_token(self, client, db_session, setup_database):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code in [401, 403]

    def test_get_current_user_no_token(self, client, db_session, setup_database):
        """Test getting current user without token."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code in [401, 403]


class TestTokenRefresh:
    """Test token refresh functionality."""

    def test_refresh_token_success(self, client, db_session, setup_database, sample_user_token):
        """Test successful token refresh."""
        headers = {"Authorization": f"Bearer {sample_user_token}"}
        response = client.post("/api/v1/auth/refresh", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_token_invalid(self, client, db_session, setup_database):
        """Test token refresh with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.post("/api/v1/auth/refresh", headers=headers)
        
        assert response.status_code in [401, 403]


class TestPasswordService:
    """Test password service functionality."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "TestPassword@123"
        hashed = password_service.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "TestPassword@123"
        hashed = password_service.hash_password(password)
        
        assert password_service.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "TestPassword@123"
        wrong_password = "WrongPassword@123"
        hashed = password_service.hash_password(password)
        
        assert password_service.verify_password(wrong_password, hashed) is False

    def test_validate_password_strength_strong(self):
        """Test password strength validation with strong password."""
        password = "StrongPassword@123"
        is_valid, error = password_service.validate_password_strength(password)
        
        assert is_valid is True
        assert error is None

    def test_validate_password_strength_weak(self):
        """Test password strength validation with weak password."""
        password = "123"
        is_valid, error = password_service.validate_password_strength(password)
        
        assert is_valid is False
        assert error is not None


class TestJWTService:
    """Test JWT service functionality."""

    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)

    def test_verify_token_valid(self):
        """Test token verification with valid token."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data)
        
        payload = jwt_service.verify_token(token)
        assert payload is not None
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"

    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        token = "invalid_token"
        
        with pytest.raises(HTTPException):
            jwt_service.verify_token(token)

    def test_get_token_expiration(self):
        """Test token expiration time."""
        data = {"sub": "123", "email": "test@example.com"}
        token = jwt_service.create_access_token(data)
        
        payload = jwt_service.verify_token(token)
        assert "exp" in payload
