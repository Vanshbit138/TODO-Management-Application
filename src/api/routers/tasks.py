"""
Task management router module.

This module defines FastAPI routes for task management including CRUD operations,
search, filtering, and other task-related endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.dependencies import get_current_active_user
from ...repositories.task_repository import TaskRepository
from ...services.task_management.task_service import TaskService
from ...schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, 
    TaskSearch, TaskFilter
)
from ...models.user import User
from ...models.task import TaskStatus

# Initialize router
router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_repository() -> TaskRepository:
    """Dependency to get task repository."""
    return TaskRepository()


def get_task_service(task_repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    """Dependency to get task service."""
    return TaskService(task_repo)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Create a new task.
    
    Args:
        task_data: Task creation data
        db: Database session
        current_user: Current authenticated user
        task_service: Task service
        
    Returns:
        TaskResponse: Created task information
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        task = task_service.create_task(
            db=db,
            owner_id=current_user.id,
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date
        )
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during task creation"
        )


@router.get("/", response_model=TaskListResponse)
async def get_tasks(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    status: Optional[TaskStatus] = Query(default=None, description="Filter by task status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get tasks for the current user with optional filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Optional status filter
        db: Database session
        current_user: Current authenticated user
        task_service: Task service
        
    Returns:
        TaskListResponse: List of tasks with metadata
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        tasks = task_service.get_tasks(
            db=db,
            owner_id=current_user.id,
            skip=skip,
            limit=limit,
            status=status
        )
        
        # Get total count for pagination
        all_tasks = task_service.get_tasks(db=db, owner_id=current_user.id, skip=0, limit=10000)
        total = len(all_tasks)
        
        task_responses = [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                due_date=task.due_date,
                owner_id=task.owner_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
        
        return TaskListResponse(
            tasks=task_responses,
            total=total,
            skip=skip,
            limit=limit
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during task retrieval"
        )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get a specific task by ID.
    
    Args:
        task_id: Task ID
        db: Database session
        current_user: Current authenticated user
        task_service: Task service
        
    Returns:
        TaskResponse: Task information
        
    Raises:
        HTTPException: If task not found or access denied
    """
    try:
        task = task_service.get_task(db=db, task_id=task_id, owner_id=current_user.id)
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during task retrieval"
        )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Update a specific task.
    
    Args:
        task_id: Task ID
        task_data: Task update data
        db: Database session
        current_user: Current authenticated user
        task_service: Task service
        
    Returns:
        TaskResponse: Updated task information
        
    Raises:
        HTTPException: If update fails or task not found
    """
    try:
        task = task_service.update_task(
            db=db,
            task_id=task_id,
            owner_id=current_user.id,
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            due_date=task_data.due_date
        )
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            due_date=task.due_date,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during task update"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Delete a specific task.
    
    Args:
        task_id: Task ID
        db: Database session
        current_user: Current authenticated user
        task_service: Task service
        
    Raises:
        HTTPException: If deletion fails or task not found
    """
    try:
        task_service.delete_task(db=db, task_id=task_id, owner_id=current_user.id)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during task deletion"
        )


@router.post("/search", response_model=TaskListResponse)
async def search_tasks(
    search_data: TaskSearch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Search tasks by title or description.
    
    Args:
        search_data: Search parameters
        db: Database session
        current_user: Current authenticated user
        task_service: Task service
        
    Returns:
        TaskListResponse: List of matching tasks
        
    Raises:
        HTTPException: If search fails
    """
    try:
        tasks = task_service.search_tasks(
            db=db,
            owner_id=current_user.id,
            search_term=search_data.search_term,
            skip=search_data.skip,
            limit=search_data.limit
        )
        
        task_responses = [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                due_date=task.due_date,
                owner_id=task.owner_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
        
        return TaskListResponse(
            tasks=task_responses,
            total=len(task_responses),
            skip=search_data.skip,
            limit=search_data.limit
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during task search"
        )


@router.get("/overdue/list", response_model=TaskListResponse)
async def get_overdue_tasks(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get overdue tasks for the current user.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated user
        task_service: Task service
        
    Returns:
        TaskListResponse: List of overdue tasks
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        tasks = task_service.get_overdue_tasks(
            db=db,
            owner_id=current_user.id,
            skip=skip,
            limit=limit
        )
        
        task_responses = [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                due_date=task.due_date,
                owner_id=task.owner_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
        
        return TaskListResponse(
            tasks=task_responses,
            total=len(task_responses),
            skip=skip,
            limit=limit
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during overdue tasks retrieval"
        )


@router.get("/due/list", response_model=TaskListResponse)
async def get_tasks_by_due_date(
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """
    Get tasks ordered by due date for the current user.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Current authenticated user
        task_service: Task service
        
    Returns:
        TaskListResponse: List of tasks ordered by due date
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        tasks = task_service.get_tasks_by_due_date(
            db=db,
            owner_id=current_user.id,
            skip=skip,
            limit=limit
        )
        
        task_responses = [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                due_date=task.due_date,
                owner_id=task.owner_id,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
        
        return TaskListResponse(
            tasks=task_responses,
            total=len(task_responses),
            skip=skip,
            limit=limit
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during tasks retrieval"
        )
