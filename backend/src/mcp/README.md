# MCP (Model Context Protocol) Server

This directory contains the implementation of the MCP server that exposes tools for AI agents to interact with the todo system.

## Overview

The MCP server provides a standardized interface for AI agents to perform todo operations through a set of well-defined tools. Each tool follows the same pattern:
- Stateless operation
- Direct database interaction
- Consistent input/output schema
- Proper error handling

## Available Tools

### 1. `add_task`
Creates a new task for a user.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "integer", "description": "The ID of the user"},
    "title": {"type": "string", "description": "The title of the task"},
    "description": {"type": "string", "description": "Optional description of the task"}
  },
  "required": ["user_id", "title"]
}
```

**Output:**
```json
{
  "success": true,
  "task_id": 123,
  "title": "Task title",
  "completed": false,
  "message": "Task 'Task title' created successfully"
}
```

### 2. `list_tasks`
Returns tasks for a user filtered by status.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "integer", "description": "The ID of the user"},
    "status": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "description": "Filter tasks by status"
    }
  },
  "required": ["user_id"]
}
```

**Output:**
```json
{
  "success": true,
  "tasks": [...],
  "count": 5,
  "status_filter": "all"
}
```

### 3. `complete_task`
Marks a specified task as complete.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "integer", "description": "The ID of the user"},
    "task_id": {"type": "integer", "description": "The ID of the task to complete"}
  },
  "required": ["user_id", "task_id"]
}
```

**Output:**
```json
{
  "success": true,
  "task_id": 123,
  "title": "Task title",
  "completed": true,
  "message": "Task 'Task title' marked as complete"
}
```

### 4. `delete_task`
Removes a specified task.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "integer", "description": "The ID of the user"},
    "task_id": {"type": "integer", "description": "The ID of the task to delete"}
  },
  "required": ["user_id", "task_id"]
}
```

**Output:**
```json
{
  "success": true,
  "task_id": 123,
  "title": "Task title",
  "message": "Task 'Task title' deleted successfully"
}
```

### 5. `update_task`
Updates task details.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "user_id": {"type": "integer", "description": "The ID of the user"},
    "task_id": {"type": "integer", "description": "The ID of the task to update"},
    "title": {"type": "string", "description": "New title for the task (optional)"},
    "description": {"type": "string", "description": "New description for the task (optional)"}
  },
  "required": ["user_id", "task_id"]
}
```

**Output:**
```json
{
  "success": true,
  "task_id": 123,
  "title": "Updated task title",
  "description": "Updated description",
  "message": "Task 'Updated task title' updated successfully"
}
```

## Architecture

- **`server.py`**: Main MCP server implementation with tool registration and orchestration
- **`tools.py`**: Individual tool implementations with database operations
- **Stateless Design**: Each tool call operates independently without maintaining session state
- **Database Integration**: Direct SQLModel integration for efficient database operations

## Usage

```python
from src.mcp.server import mcp_server

# Get available tools
available_tools = mcp_server.get_tool_list()

# Call a specific tool
result = await mcp_server.call_tool('add_task', {
    'user_id': 1,
    'title': 'New task',
    'description': 'Task description'
})
```

## Error Handling

All tools follow a consistent error handling pattern:
- Validation of required parameters
- Database operation errors
- User permission checks
- Non-existent record handling

Errors are returned in the format:
```json
{
  "success": false,
  "error": "Error message"
}
```