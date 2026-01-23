"""
MCP Tools Implementation
Contains the actual implementations for all MCP tools
"""

import asyncio
from typing import Dict, Any, Optional
from sqlmodel import Session, select
from src.models.user_task_models import Task
from src.database.session import engine


async def add_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to add a new task to the database
    Expected params: {'user_id': int, 'title': str, 'description': str (optional)}
    """
    user_id = params.get('user_id')
    title = params.get('title')
    description = params.get('description')

    if not user_id or not title:
        return {
            'success': False,
            'error': 'Missing required parameters: user_id and title are required'
        }

    try:
        with Session(engine) as session:
            # Create new task
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                'success': True,
                'task_id': task.id,
                'title': task.title,
                'completed': task.completed,
                'message': f'Task "{task.title}" created successfully'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


async def list_tasks_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to list tasks for a user
    Expected params: {'user_id': int, 'status': str ('all', 'pending', 'completed')}
    """
    user_id = params.get('user_id')
    status = params.get('status', 'all')  # Default to 'all'

    if not user_id:
        return {
            'success': False,
            'error': 'Missing required parameter: user_id is required'
        }

    try:
        with Session(engine) as session:
            # Build query based on status
            query = select(Task).where(Task.user_id == user_id)

            if status == 'pending':
                query = query.where(Task.completed == False)
            elif status == 'completed':
                query = query.where(Task.completed == True)
            # If status is 'all', no additional filter needed

            tasks = session.exec(query).all()

            task_list = [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority,
                    'due_date': task.due_date.isoformat() if task.due_date else None,
                    'created_at': task.created_at.isoformat(),
                    'updated_at': task.updated_at.isoformat()
                }
                for task in tasks
            ]

            return {
                'success': True,
                'tasks': task_list,
                'count': len(task_list),
                'status_filter': status
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


async def complete_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to mark a task as complete
    Expected params: {'user_id': int, 'task_id': int}
    """
    user_id = params.get('user_id')
    task_id = params.get('task_id')

    if not user_id or not task_id:
        return {
            'success': False,
            'error': 'Missing required parameters: user_id and task_id are required'
        }

    try:
        with Session(engine) as session:
            # Find the task for the specific user
            task = session.exec(
                select(Task).where(Task.user_id == user_id).where(Task.id == task_id)
            ).first()

            if not task:
                return {
                    'success': False,
                    'error': f'Task with ID {task_id} not found for user {user_id}'
                }

            # Update task completion status
            task.completed = True
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                'success': True,
                'task_id': task.id,
                'title': task.title,
                'completed': task.completed,
                'message': f'Task "{task.title}" marked as complete'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


async def delete_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to delete a task
    Expected params: {'user_id': int, 'task_id': int}
    """
    user_id = params.get('user_id')
    task_id = params.get('task_id')

    if not user_id or not task_id:
        return {
            'success': False,
            'error': 'Missing required parameters: user_id and task_id are required'
        }

    try:
        with Session(engine) as session:
            # Find the task for the specific user
            task = session.exec(
                select(Task).where(Task.user_id == user_id).where(Task.id == task_id)
            ).first()

            if not task:
                return {
                    'success': False,
                    'error': f'Task with ID {task_id} not found for user {user_id}'
                }

            # Delete the task
            session.delete(task)
            session.commit()

            return {
                'success': True,
                'task_id': task_id,
                'title': task.title,
                'message': f'Task "{task.title}" deleted successfully'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


async def update_task_tool(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Tool to update task details
    Expected params: {'user_id': int, 'task_id': int, 'title': str (optional), 'description': str (optional)}
    """
    user_id = params.get('user_id')
    task_id = params.get('task_id')
    title = params.get('title')
    description = params.get('description')

    if not user_id or not task_id:
        return {
            'success': False,
            'error': 'Missing required parameters: user_id and task_id are required'
        }

    try:
        with Session(engine) as session:
            # Find the task for the specific user
            task = session.exec(
                select(Task).where(Task.user_id == user_id).where(Task.id == task_id)
            ).first()

            if not task:
                return {
                    'success': False,
                    'error': f'Task with ID {task_id} not found for user {user_id}'
                }

            # Update task details if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                'success': True,
                'task_id': task.id,
                'title': task.title,
                'description': task.description,
                'message': f'Task "{task.title}" updated successfully'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }