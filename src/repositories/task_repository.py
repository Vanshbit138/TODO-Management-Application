"""
Task data operations module.

This module implements the TaskRepository for task-related database operations.
It handles CRUD operations for tasks, filtering, and other task-related data access functionality.
"""

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..models.task import Task, TaskStatus


class TaskRepository:
    """Repository for task data access operations."""
    
    def create_task(self, db: Session, task_data: Dict[str, Any]) -> Task:
        """
        Create a new task.
        
        Args:
            db: Database session
            task_data: Task data dictionary
            
        Returns:
            Task: Created task object
        """
        task = Task(**task_data)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def get_task_by_id(self, db: Session, task_id: int, owner_id: int) -> Optional[Task]:
        """
        Get task by ID for a specific owner.
        
        Args:
            db: Database session
            task_id: Task ID
            owner_id: Owner user ID
            
        Returns:
            Optional[Task]: Task object if found, None otherwise
        """
        return db.query(Task).filter(
            and_(Task.id == task_id, Task.owner_id == owner_id)
        ).first()
    
    def get_tasks_by_owner(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all tasks for a specific owner with pagination.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of task objects
        """
        return db.query(Task).filter(Task.owner_id == owner_id).offset(skip).limit(limit).all()
    
    def get_tasks_by_status(self, db: Session, owner_id: int, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get tasks by status for a specific owner.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            status: Task status
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of task objects
        """
        return db.query(Task).filter(
            and_(Task.owner_id == owner_id, Task.status == status)
        ).offset(skip).limit(limit).all()
    
    def get_tasks_by_due_date(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get tasks ordered by due date for a specific owner.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of task objects ordered by due date
        """
        return db.query(Task).filter(Task.owner_id == owner_id).order_by(Task.due_date.asc()).offset(skip).limit(limit).all()
    
    def update_task(self, db: Session, task_id: int, owner_id: int, task_data: Dict[str, Any]) -> Optional[Task]:
        """
        Update task data.
        
        Args:
            db: Database session
            task_id: Task ID
            owner_id: Owner user ID
            task_data: Updated task data
            
        Returns:
            Optional[Task]: Updated task object if found, None otherwise
        """
        task = self.get_task_by_id(db, task_id, owner_id)
        if not task:
            return None
        
        for key, value in task_data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        db.commit()
        db.refresh(task)
        return task
    
    def delete_task(self, db: Session, task_id: int, owner_id: int) -> bool:
        """
        Delete task by ID for a specific owner.
        
        Args:
            db: Database session
            task_id: Task ID
            owner_id: Owner user ID
            
        Returns:
            bool: True if task was deleted, False otherwise
        """
        task = self.get_task_by_id(db, task_id, owner_id)
        if not task:
            return False
        
        db.delete(task)
        db.commit()
        return True
    
    def search_tasks(self, db: Session, owner_id: int, search_term: str, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Search tasks by title or description for a specific owner.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of matching task objects
        """
        return db.query(Task).filter(
            and_(
                Task.owner_id == owner_id,
                or_(
                    Task.title.contains(search_term),
                    Task.description.contains(search_term)
                )
            )
        ).offset(skip).limit(limit).all()
    
    def get_overdue_tasks(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Get overdue tasks for a specific owner.
        
        Args:
            db: Database session
            owner_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Task]: List of overdue task objects
        """
        from datetime import datetime
        return db.query(Task).filter(
            and_(
                Task.owner_id == owner_id,
                Task.due_date < datetime.utcnow(),
                Task.status != TaskStatus.COMPLETED
            )
        ).offset(skip).limit(limit).all()
