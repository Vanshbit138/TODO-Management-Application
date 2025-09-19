"""
FastAPI dependencies module.

This module contains reusable FastAPI dependencies for authentication,
database access, and other common functionality across the application.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from ..repositories.user_repository import UserRepository
from ..services.authentication.auth_service import AuthenticationService
from ..services.authentication.jwt_service import jwt_service
from ..models.user import User

# Security scheme
security = HTTPBearer()


def get_user_repository() -> UserRepository:
    """Dependency to get user repository."""
    return UserRepository()


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthenticationService:
    """Dependency to get authentication service."""
    return AuthenticationService(user_repo)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> User:
    """
    Dependency to get current authenticated user.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        auth_service: Authentication service
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        user = auth_service.get_current_user(db=db, token=credentials.credentials)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to get current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current active user
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


def get_current_verified_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to get current verified user.
    
    Args:
        current_user: Current active user
        
    Returns:
        User: Current verified user
        
    Raises:
        HTTPException: If user is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not verified"
        )
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> Optional[User]:
    """
    Dependency to get current user (optional authentication).
    
    Args:
        credentials: Optional HTTP Bearer token credentials
        db: Database session
        auth_service: Authentication service
        
    Returns:
        Optional[User]: Current user if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    try:
        user = auth_service.get_current_user(db=db, token=credentials.credentials)
        return user
    except HTTPException:
        return None
    except Exception:
        return None
