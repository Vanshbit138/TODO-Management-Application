"""
Authentication service module.

This module provides authentication business logic including user registration,
login, and token management. It handles user validation, password verification,
and JWT token generation for authenticated users.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ...models.user import User
from ...repositories.user_repository import UserRepository
from .password_service import password_service
from .jwt_service import jwt_service


class AuthenticationService:
    """Service for user authentication operations."""
    
    def __init__(self, user_repository: UserRepository):
        """
        Initialize authentication service.
        
        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository
    
    def register_user(self, db: Session, email: str, username: str, password: str, full_name: Optional[str] = None) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            email: User email address
            username: Username
            password: Plain text password
            full_name: Optional full name
            
        Returns:
            User: Created user object
            
        Raises:
            HTTPException: If user already exists or validation fails
        """
        # Validate password strength
        is_valid, error_message = password_service.validate_password_strength(password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Check if user already exists
        existing_user = self.user_repository.get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_user = self.user_repository.get_user_by_username(db, username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Hash password
        hashed_password = password_service.hash_password(password)
        
        # Create user
        user_data = {
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "full_name": full_name,
            "is_active": True,
            "is_verified": False
        }
        
        user = self.user_repository.create_user(db, user_data)
        return user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            Optional[User]: User object if authentication successful, None otherwise
        """
        user = self.user_repository.get_user_by_email(db, email)
        if not user:
            return None
        
        if not password_service.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def login_user(self, db: Session, email: str, password: str) -> Dict[str, Any]:
        """
        Login a user and return access token.
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            Dict[str, Any]: Access token and user information
            
        Raises:
            HTTPException: If authentication fails
        """
        user = self.authenticate_user(db, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = None  # Use default expiration
        access_token = jwt_service.create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "is_verified": user.is_verified
            }
        }
    
    def get_current_user(self, db: Session, token: str) -> User:
        """
        Get current user from JWT token.
        
        Args:
            db: Database session
            token: JWT access token
            
        Returns:
            User: Current user object
            
        Raises:
            HTTPException: If token is invalid or user not found
        """
        user_id = jwt_service.get_user_id_from_token(token)
        user = self.user_repository.get_user_by_id(db, user_id)
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
