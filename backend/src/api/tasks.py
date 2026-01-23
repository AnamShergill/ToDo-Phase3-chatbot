from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from ..database.session import get_session
from ..schemas.task_schemas import (
    TaskCreate, TaskUpdate, TaskComplete, TaskResponse,
    TaskListResponse, TaskDetailResponse, SuccessResponse
)
from ..services.task_service import TaskService
from ..middleware.auth import verify_token
from datetime import datetime

router = APIRouter(prefix="/api/{user_id}")


@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    user_id: int,
    authenticated_user_id: int = Depends(verify_token),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query("all", pattern="^(all|completed|pending)$"),
    priority: Optional[str] = Query(None, pattern="^(low|medium|high)$"),
    sort: str = Query("created", pattern="^(created|due_date|priority)$"),
    db: Session = Depends(get_session)
):
    """
    Retrieve all tasks for the authenticated user with optional filtering and pagination.
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's tasks"
        )

    task_service = TaskService(db)

    # Get tasks with applied filters
    tasks = task_service.get_tasks_by_user(
        user_id=authenticated_user_id,
        skip=skip,
        limit=limit,
        status=status,
        priority=priority,
        sort=sort
    )

    # Get total count for pagination
    total_count = task_service.get_task_count_by_user(authenticated_user_id, status)
    total_pages = (total_count + limit - 1) // limit

    # Convert tasks to response format
    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        task_responses.append(task_response)

    return TaskListResponse(
        success=True,
        data={
            "tasks": task_responses,
            "pagination": {
                "page": skip // limit + 1,
                "limit": limit,
                "total": total_count,
                "total_pages": total_pages
            }
        }
    )


@router.post("/tasks", response_model=TaskDetailResponse, status_code=201)
async def create_task(
    user_id: int,
    task_data: TaskCreate,
    authenticated_user_id: int = Depends(verify_token),
    db: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create tasks for this user"
        )

    task_service = TaskService(db)

    # Validate that title is not empty
    if not task_data.title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")

    try:
        task = task_service.create_task(authenticated_user_id, task_data)

        task_response = TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

        return TaskDetailResponse(
            success=True,
            data=task_response,
            message="Task created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create task: {str(e)}")


@router.get("/tasks/{task_id}", response_model=TaskDetailResponse)
async def get_task(
    user_id: int,
    task_id: int,
    authenticated_user_id: int = Depends(verify_token),
    db: Session = Depends(get_session)
):
    """
    Retrieve a specific task by ID for the authenticated user.
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's tasks"
        )

    task_service = TaskService(db)

    task = task_service.get_task_by_id(authenticated_user_id, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_response = TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        due_date=task.due_date,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

    return TaskDetailResponse(
        success=True,
        data=task_response
    )


@router.put("/tasks/{task_id}", response_model=TaskDetailResponse)
async def update_task(
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    authenticated_user_id: int = Depends(verify_token),
    db: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this user's tasks"
        )

    task_service = TaskService(db)

    updated_task = task_service.update_task(authenticated_user_id, task_id, task_data)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to user")

    task_response = TaskResponse(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        priority=updated_task.priority,
        due_date=updated_task.due_date,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )

    return TaskDetailResponse(
        success=True,
        data=task_response,
        message="Task updated successfully"
    )


@router.patch("/tasks/{task_id}/complete", response_model=TaskDetailResponse)
async def update_task_completion(
    user_id: int,
    task_id: int,
    completion_data: TaskComplete,
    authenticated_user_id: int = Depends(verify_token),
    db: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task.
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this user's tasks"
        )

    task_service = TaskService(db)

    updated_task = task_service.update_task_completion(authenticated_user_id, task_id, completion_data)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to user")

    task_response = TaskResponse(
        id=updated_task.id,
        user_id=updated_task.user_id,
        title=updated_task.title,
        description=updated_task.description,
        completed=updated_task.completed,
        priority=updated_task.priority,
        due_date=updated_task.due_date,
        created_at=updated_task.created_at,
        updated_at=updated_task.updated_at
    )

    return TaskDetailResponse(
        success=True,
        data=task_response,
        message="Task completion status updated successfully"
    )


@router.delete("/tasks/{task_id}", response_model=SuccessResponse)
async def delete_task(
    user_id: int,
    task_id: int,
    authenticated_user_id: int = Depends(verify_token),
    db: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    """
    # Verify that the requested user_id matches the authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this user's tasks"
        )

    task_service = TaskService(db)

    deleted = task_service.delete_task(authenticated_user_id, task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to user")

    return SuccessResponse(
        success=True,
        data={"message": "Task deleted successfully"}
    )