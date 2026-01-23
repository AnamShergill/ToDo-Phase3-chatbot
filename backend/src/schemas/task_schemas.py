from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"  # "low", "medium", "high"
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TaskComplete(BaseModel):
    completed: bool


class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    success: bool
    data: dict
    message: Optional[str] = None


class TaskDetailResponse(BaseModel):
    success: bool
    data: TaskResponse
    message: Optional[str] = None


class SuccessResponse(BaseModel):
    success: bool
    data: dict
    message: Optional[str] = None