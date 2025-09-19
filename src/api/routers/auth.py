"""
Authentication router module.

This module defines FastAPI routes for user authentication including registration,
login, and token management. It handles HTTP requests and responses for auth operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...repositories.user_repository import UserRepository
from ...services.authentication.auth_service import AuthenticationService
from ...schemas.auth import UserRegistration, UserLogin, TokenResponse, UserResponse

# Initialize router
router = APIRouter(prefix="/auth", tags=["authentication"])

# Security scheme
security = HTTPBearer()


def get_user_repository() -> UserRepository:
    """Dependency to get user repository."""
    return UserRepository()


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthenticationService:
    """Dependency to get authentication service."""
    return AuthenticationService(user_repo)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegistration,
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        auth_service: Authentication service
        
    Returns:
        UserResponse: Created user information
        
    Raises:
        HTTPException: If registration fails
    """
    try:
        user = auth_service.register_user(
            db=db,
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name
        )
        
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Login user and return access token.
    
    Args:
        login_data: User login credentials
        db: Database session
        auth_service: Authentication service
        
    Returns:
        TokenResponse: Access token and user information
        
    Raises:
        HTTPException: If login fails
    """
    try:
        result = auth_service.login_user(
            db=db,
            email=login_data.email,
            password=login_data.password
        )
        
        return TokenResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Get current authenticated user information.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        auth_service: Authentication service
        
    Returns:
        UserResponse: Current user information
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        user = auth_service.get_current_user(db=db, token=credentials.credentials)
        
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Refresh access token.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        auth_service: Authentication service
        
    Returns:
        TokenResponse: New access token and user information
        
    Raises:
        HTTPException: If token refresh fails
    """
    try:
        user = auth_service.get_current_user(db=db, token=credentials.credentials)
        
        # Create new token
        from ...services.authentication.jwt_service import jwt_service
        access_token = jwt_service.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified
            )
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        )
