"""
Task management service module.

This module provides task business logic including CRUD operations,
task validation, and task management functionality.
"""

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime

from ...models.task import Task, TaskStatus
from ...repositories.task_repository import TaskRepository


class TaskService:
    """Service for task management operations."""
    
    def __init__(self, task_repository: TaskRepository):
        """
        Initialize task service.
        
        Args:
            task_repository: Repository for task data access
        """
        self.task_repository = task_repository
    
    def create_task(self, db: Session, owner_id: int, title: str, description: Optional[str] = None, 
                   due_date: Optional[datetime] = None) -> Task:
        """
        Create a new task.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            title: Task title
            description: Optional task description
            due_date: Optional due date
            
        Returns:
            Task: Created task object
            
        Raises:
            HTTPException: If validation fails
        """
        # Validate title
        if not title or len(title.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title is required"
            )
        
        if len(title) > 255:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task title must be less than 255 characters"
            )
        
        # Validate description
        if description and len(description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task description must be less than 1000 characters"
            )
        
        # Validate due date
        if due_date and due_date < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Due date cannot be in the past"
            )
        
        # Create task data
        task_data = {
            "title": title.strip(),
            "description": description.strip() if description else None,
            "status": TaskStatus.TODO,
            "due_date": due_date,
            "owner_id": owner_id
        }
        
        task = self.task_repository.create_task(db, task_data)
        return task
    
    def get_task(self, db: Session, task_id: int, owner_id: int) -> Task:
        """
        Get a specific task.
        
        Args:
            db: Database session
            task_id: Task ID
            owner_id: Owner user ID
            
        Returns:
            Task: Task object
            
        Raises:
            HTTPException: If task not found
        """
        task = self.task_repository.get_task_by_id(db, task_id, owner_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return task
    
    def get_tasks(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100, 
                  status: Optional[TaskStatus] = None) -> List[Task]:
        """
        Get tasks for a user with optional filtering.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Optional status filter
            
        Returns:
            List[Task]: List of task objects
        """
        if status:
            return self.task_repository.get_tasks_by_status(db, owner_id, status, skip, limit)
        else:
            return self.task_repository.get_tasks_by_owner(db, owner_id, skip, limit)
    
    def update_task(self, db: Session, task_id: int, owner_id: int, 
                   title: Optional[str] = None, description: Optional[str] = None,
                   status: Optional[TaskStatus] = None, due_date: Optional[datetime] = None) -> Task:
        """
        Update a task.
        
        Args:
            db: Database session
            task_id: Task ID
            owner_id: Owner user ID
            title: Optional new title
            description: Optional new description
            status: Optional new status
            due_date: Optional new due date
            
        Returns:
            Task: Updated task object
            
        Raises:
            HTTPException: If validation fails or task not found
        """
        # Validate title if provided
        if title is not None:
            if not title or len(title.strip()) == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task title is required"
                )
            if len(title) > 255:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task title must be less than 255 characters"
                )
        
        # Validate description if provided
        if description is not None and len(description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task description must be less than 1000 characters"
            )
        
        # Validate due date if provided
        if due_date and due_date < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Due date cannot be in the past"
            )
        
        # Prepare update data
        update_data = {}
        if title is not None:
            update_data["title"] = title.strip()
        if description is not None:
            update_data["description"] = description.strip() if description else None
        if status is not None:
            update_data["status"] = status
        if due_date is not None:
            update_data["due_date"] = due_date
        
        # Update task
        task = self.task_repository.update_task(db, task_id, owner_id, update_data)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return task
    
    def delete_task(self, db: Session, task_id: int, owner_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            db: Database session
            task_id: Task ID
            owner_id: Owner user ID
            
        Returns:
            bool: True if task was deleted
            
        Raises:
            HTTPException: If task not found
        """
        success = self.task_repository.delete_task(db, task_id, owner_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        return True
    
    def search_tasks(self, db: Session, owner_id: int, search_term: str, 
                    skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Search tasks by title or description.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of matching task objects
        """
        if not search_term or len(search_term.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search term is required"
            )
        
        return self.task_repository.search_tasks(db, owner_id, search_term.strip(), skip, limit)
    
    def get_overdue_tasks(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get overdue tasks for a user.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of overdue task objects
        """
        return self.task_repository.get_overdue_tasks(db, owner_id, skip, limit)
    
    def get_tasks_by_due_date(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get tasks ordered by due date.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of task objects ordered by due date
        """
        return self.task_repository.get_tasks_by_due_date(db, owner_id, skip, limit)
