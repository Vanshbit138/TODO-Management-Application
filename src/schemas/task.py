"""
Task schemas module.

This module contains Pydantic models for task-related requests and responses.
It includes schemas for task creation, updates, and responses.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator

from ..models.task import TaskStatus


class TaskCreate(BaseModel):
    """Schema for task creation request."""
    
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    
    @validator('title')
    def validate_title(cls, v):
        """Validate task title."""
        if not v or not v.strip():
            raise ValueError('Task title cannot be empty')
        return v.strip()
    
    @validator('description')
    def validate_description(cls, v):
        """Validate task description."""
        if v is not None:
            return v.strip() if v else None
        return v
    
    @validator('due_date')
    def validate_due_date(cls, v):
        """Validate due date."""
        if v and v < datetime.utcnow():
            raise ValueError('Due date cannot be in the past')
        return v


class TaskUpdate(BaseModel):
    """Schema for task update request."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    
    @validator('title')
    def validate_title(cls, v):
        """Validate task title."""
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Task title cannot be empty')
            return v.strip()
        return v
    
    @validator('description')
    def validate_description(cls, v):
        """Validate task description."""
        if v is not None:
            return v.strip() if v else None
        return v
    
    @validator('due_date')
    def validate_due_date(cls, v):
        """Validate due date."""
        if v and v < datetime.utcnow():
            raise ValueError('Due date cannot be in the past')
        return v


class TaskResponse(BaseModel):
    """Schema for task response."""
    
    id: int = Field(..., description="Task ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(..., description="Task status")
    due_date: Optional[datetime] = Field(None, description="Task due date")
    owner_id: int = Field(..., description="Owner user ID")
    created_at: datetime = Field(..., description="Task creation date")
    updated_at: datetime = Field(..., description="Task last update date")
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for task list response."""
    
    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    skip: int = Field(..., description="Number of tasks skipped")
    limit: int = Field(..., description="Maximum number of tasks returned")


class TaskSearch(BaseModel):
    """Schema for task search request."""
    
    search_term: str = Field(..., min_length=1, max_length=100, description="Search term")
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of records to return")
    
    @validator('search_term')
    def validate_search_term(cls, v):
        """Validate search term."""
        if not v or not v.strip():
            raise ValueError('Search term cannot be empty')
        return v.strip()


class TaskFilter(BaseModel):
    """Schema for task filtering."""
    
    status: Optional[TaskStatus] = Field(None, description="Filter by task status")
    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum number of records to return")
