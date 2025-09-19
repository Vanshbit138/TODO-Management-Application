"""
Task/TODO entity model module.

This module defines the SQLAlchemy Task model for task management functionality.
It includes fields for title, description, status, priority, due dates,
and any other task-related database entities.
"""

from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..core.database import Base


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Task(Base):
    """Task model for TODO management."""
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False, index=True)
    due_date = Column(DateTime(timezone=True), nullable=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationship with user
    owner = relationship("User", back_populates="tasks")
    
    def __repr__(self) -> str:
        """String representation of Task."""
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}', owner_id={self.owner_id})>"
