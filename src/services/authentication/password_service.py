"""
Password hashing and verification service.

This module provides secure password hashing and verification using bcrypt.
It handles password hashing, verification, and strength validation for user authentication.
"""

from passlib.context import CryptContext
from typing import Optional


class PasswordService:
    """Service for password hashing and verification."""
    
    def __init__(self):
        """Initialize password service with bcrypt context."""
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password to hash
            
        Returns:
            str: Hashed password
            
        Raises:
            ValueError: If password is empty or None
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to verify against
            
        Returns:
            bool: True if password matches, False otherwise
        """
        if not plain_password or not hashed_password:
            return False
        
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def validate_password_strength(self, password: str) -> tuple[bool, Optional[str]]:
        """
        Validate password strength requirements.
        
        Args:
            password: Password to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        
        # Check for at least one uppercase letter
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for at least one lowercase letter
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for at least one digit
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        
        # Check for at least one special character
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            return False, "Password must contain at least one special character"
        
        return True, None


# Global password service instance
password_service = PasswordService()
