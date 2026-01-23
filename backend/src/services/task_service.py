from sqlmodel import Session, select, update
from ..models.user_task_models import Task, User
from ..schemas.task_schemas import TaskCreate, TaskUpdate, TaskComplete
from typing import List, Optional
from datetime import datetime


class TaskService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_task(self, user_id: int, task_data: TaskCreate) -> Task:
        """Create a new task for the specified user."""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            priority=task_data.priority,
            due_date=task_data.due_date
        )
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    def get_tasks_by_user(self, user_id: int, skip: int = 0, limit: int = 10, status: str = "all",
                         priority: Optional[str] = None, sort: str = "created") -> List[Task]:
        """Get all tasks for a specific user with optional filtering."""
        statement = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status != "all":
            if status == "completed":
                statement = statement.where(Task.completed == True)
            elif status == "pending":
                statement = statement.where(Task.completed == False)

        # Apply priority filter
        if priority:
            statement = statement.where(Task.priority == priority)

        # Apply sorting
        if sort == "due_date":
            statement = statement.order_by(Task.due_date)
        elif sort == "priority":
            statement = statement.order_by(Task.priority)
        else:  # default to created date
            statement = statement.order_by(Task.created_at.desc())

        statement = statement.offset(skip).limit(limit)
        result = self.db_session.execute(statement)
        tasks = result.scalars().all()
        return tasks

    def get_task_by_id(self, user_id: int, task_id: int) -> Optional[Task]:
        """Get a specific task by ID for the specified user."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.db_session.execute(statement)
        task = result.scalar_one_or_none()
        return task

    def update_task(self, user_id: int, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update a specific task for the specified user."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.db_session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Update task fields if they are provided in the update data
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Update the updated_at timestamp
        task.updated_at = datetime.utcnow()

        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    def update_task_completion(self, user_id: int, task_id: int, completion_data: TaskComplete) -> Optional[Task]:
        """Update the completion status of a specific task."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.db_session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        task.completed = completion_data.completed
        task.updated_at = datetime.utcnow()

        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    def delete_task(self, user_id: int, task_id: int) -> bool:
        """Delete a specific task for the specified user."""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = self.db_session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return False

        self.db_session.delete(task)
        self.db_session.commit()
        return True

    def get_task_count_by_user(self, user_id: int, status: str = "all") -> int:
        """Get the total count of tasks for a user with optional status filter."""
        statement = select(Task).where(Task.user_id == user_id)

        if status != "all":
            if status == "completed":
                statement = statement.where(Task.completed == True)
            elif status == "pending":
                statement = statement.where(Task.completed == False)

        result = self.db_session.execute(statement)
        tasks = result.scalars().all()
        return len(tasks)