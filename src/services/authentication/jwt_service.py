"""
JWT token management service.

This module handles JWT token creation, validation, and decoding for user authentication.
It provides utilities for generating access tokens, verifying tokens, and extracting user information.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status

from ...core.config import settings


class JWTService:
    """Service for JWT token operations."""
    
    def __init__(self):
        """Initialize JWT service with configuration."""
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in the token (typically user_id and email)
            expires_delta: Optional custom expiration time
            
        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Dict[str, Any]: Decoded token payload
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def get_user_id_from_token(self, token: str) -> int:
        """
        Extract user ID from JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            int: User ID from token
            
        Raises:
            HTTPException: If token is invalid or user_id is missing
        """
        payload = self.verify_token(token)
        user_id: int = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return int(user_id)
    
    def get_user_email_from_token(self, token: str) -> str:
        """
        Extract user email from JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            str: User email from token
            
        Raises:
            HTTPException: If token is invalid or email is missing
        """
        payload = self.verify_token(token)
        email: str = payload.get("email")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return email


# Global JWT service instance
jwt_service = JWTService()
