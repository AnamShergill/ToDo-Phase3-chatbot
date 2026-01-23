"""
MCP (Model Context Protocol) Server Implementation
Exposes tools for AI agents to interact with the todo system
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from fastapi import HTTPException
from sqlmodel import Session, select
from src.models.user_task_models import Task
from src.database.session import engine
from src.mcp.tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool


class MCPServer:
    """
    MCP Server that manages tools for AI agent interaction
    """

    def __init__(self):
        self.tools = {}
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools"""
        self.tools['add_task'] = {
            'name': 'add_task',
            'description': 'Creates a new task for a user',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer', 'description': 'The ID of the user'},
                    'title': {'type': 'string', 'description': 'The title of the task'},
                    'description': {'type': 'string', 'description': 'Optional description of the task'}
                },
                'required': ['user_id', 'title']
            }
        }

        self.tools['list_tasks'] = {
            'name': 'list_tasks',
            'description': 'Returns tasks for a user filtered by status',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer', 'description': 'The ID of the user'},
                    'status': {
                        'type': 'string',
                        'enum': ['all', 'pending', 'completed'],
                        'description': 'Filter tasks by status'
                    }
                },
                'required': ['user_id']
            }
        }

        self.tools['complete_task'] = {
            'name': 'complete_task',
            'description': 'Marks a specified task as complete',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer', 'description': 'The ID of the user'},
                    'task_id': {'type': 'integer', 'description': 'The ID of the task to complete'}
                },
                'required': ['user_id', 'task_id']
            }
        }

        self.tools['delete_task'] = {
            'name': 'delete_task',
            'description': 'Removes a specified task',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer', 'description': 'The ID of the user'},
                    'task_id': {'type': 'integer', 'description': 'The ID of the task to delete'}
                },
                'required': ['user_id', 'task_id']
            }
        }

        self.tools['update_task'] = {
            'name': 'update_task',
            'description': 'Updates task details',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer', 'description': 'The ID of the user'},
                    'task_id': {'type': 'integer', 'description': 'The ID of the task to update'},
                    'title': {'type': 'string', 'description': 'New title for the task (optional)'},
                    'description': {'type': 'string', 'description': 'New description for the task (optional)'}
                },
                'required': ['user_id', 'task_id']
            }
        }

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a specific tool with the provided parameters
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        try:
            if tool_name == 'add_task':
                return await add_task_tool(parameters)
            elif tool_name == 'list_tasks':
                return await list_tasks_tool(parameters)
            elif tool_name == 'complete_task':
                return await complete_task_tool(parameters)
            elif tool_name == 'delete_task':
                return await delete_task_tool(parameters)
            elif tool_name == 'update_task':
                return await update_task_tool(parameters)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }

    def get_tool_list(self) -> List[Dict[str, Any]]:
        """Return a list of available tools"""
        return list(self.tools.values())


# Global MCP server instance
mcp_server = MCPServer()