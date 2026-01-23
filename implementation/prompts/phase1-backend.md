# Phase 1 Implementation Prompts

## Database Implementation Prompt

**Task**: Implement tasks table in Neon PostgreSQL following @specs/database/schema.md

**Instructions for Claude Code**:
- Read the database schema specification at @specs/database/schema.md
- Create the User and Task models in backend/src/models/
- Implement the database connection setup for Neon PostgreSQL
- Create Alembic migration files for the database schema
- Ensure all constraints, indexes, and relationships are properly defined
- Follow the SQLModel ORM patterns for model definitions
- Include proper validation and error handling

## FastAPI Routes Implementation Prompt

**Task**: Implement all task CRUD FastAPI routes following @specs/api/rest-endpoints.md

**Instructions for Claude Code**:
- Read the API endpoint specification at @specs/api/rest-endpoints.md
- Create the task API endpoints in backend/src/api/tasks.py
- Implement GET /api/{user_id}/tasks for listing tasks
- Implement POST /api/{user_id}/tasks for creating tasks
- Implement GET /api/{user_id}/tasks/{id} for getting a specific task
- Implement PUT /api/{user_id}/tasks/{id} for updating tasks
- Implement PATCH /api/{user_id}/tasks/{id}/complete for toggling completion
- Implement DELETE /api/{user_id}/tasks/{id} for deleting tasks
- Include proper request/response validation
- Add appropriate error handling and status codes
- Ensure all endpoints return responses in the format specified in the API spec

## Task CRUD Features Implementation Prompt

**Task**: Implement create/read/update/delete/complete features following @specs/features/task-crud.md

**Instructions for Claude Code**:
- Read the task CRUD feature specification at @specs/features/task-crud.md
- Create a TaskService in backend/src/services/task_service.py
- Implement proper validation logic for all CRUD operations
- Ensure user isolation (users can only access their own tasks)
- Implement business logic for task completion toggling
- Add appropriate logging and error handling
- Create unit tests for the service layer
- Ensure all acceptance criteria from the spec are met
- Include proper authentication checks if needed at the service level