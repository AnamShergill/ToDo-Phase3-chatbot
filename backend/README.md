# Todo Backend API

This is the backend API for the Todo Full-Stack Web Application. It provides REST endpoints for managing tasks with user isolation.

## Tech Stack

- FastAPI: Web framework
- SQLModel: ORM for database operations
- PostgreSQL: Database (Neon-compatible)
- Pydantic: Data validation

## Features

- Task CRUD operations (Create, Read, Update, Delete)
- Task completion toggling
- User-specific task isolation
- Filtering and pagination
- Proper error handling

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment file and configure your database:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## API Endpoints

All endpoints follow the pattern `/api/{user_id}/tasks` where `{user_id}` identifies the user whose tasks are being accessed.

- `GET /api/{user_id}/tasks` - Get all tasks for a user (with optional filtering)
- `POST /api/{user_id}/tasks` - Create a new task for a user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task

## Database Schema

The application uses two main tables:

### users table
- id (INTEGER, PRIMARY KEY)
- email (VARCHAR, UNIQUE)
- password_hash (VARCHAR)
- name (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### tasks table
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY to users.id)
- title (VARCHAR, NOT NULL)
- description (TEXT, NULL)
- completed (BOOLEAN, DEFAULT FALSE)
- priority (VARCHAR, DEFAULT 'medium')
- due_date (TIMESTAMP, NULL)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

## Authentication

Note: JWT authentication will be implemented in Phase 2. Currently, the user_id is passed as a path parameter for demonstration purposes.