"""
User data operations module.

This module implements the UserRepository for user-related database operations.
It handles CRUD operations for users, authentication queries, user validation,
and other user-related data access functionality.
"""

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.user import User


class UserRepository:
    """Repository for user data access operations."""
    
    def create_user(self, db: Session, user_data: Dict[str, Any]) -> User:
        """
        Create a new user.
        
        Args:
            db: Database session
            user_data: User data dictionary
            
        Returns:
            User: Created user object
        """
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            db: Database session
            username: Username
            
        Returns:
            Optional[User]: User object if found, None otherwise
        """
        return db.query(User).filter(User.username == username).first()
    
    def get_all_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of user objects
        """
        return db.query(User).offset(skip).limit(limit).all()
    
    def update_user(self, db: Session, user_id: int, user_data: Dict[str, Any]) -> Optional[User]:
        """
        Update user data.
        
        Args:
            db: Database session
            user_id: User ID
            user_data: Updated user data
            
        Returns:
            Optional[User]: Updated user object if found, None otherwise
        """
        user = self.get_user_by_id(db, user_id)
        if not user:
            return None
        
        for key, value in user_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    def delete_user(self, db: Session, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            bool: True if user was deleted, False otherwise
        """
        user = self.get_user_by_id(db, user_id)
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True
    
    def get_active_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all active users with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of active user objects
        """
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def get_verified_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all verified users with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of verified user objects
        """
        return db.query(User).filter(User.is_verified == True).offset(skip).limit(limit).all()
