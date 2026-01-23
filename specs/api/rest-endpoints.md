# REST API Endpoints Specification

## API Overview

The Todo application provides a RESTful API with JWT-secured endpoints for all CRUD operations. All endpoints follow standard REST conventions and require valid authentication tokens for access to user-specific data.

## Base URL

All API endpoints are prefixed with `/api` and follow the pattern:
`https://[domain]/api/{user_id}/tasks`

## Authentication

All endpoints (except authentication-specific ones) require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional descriptive message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "details": { ... }
}
```

## Endpoints

### Authentication Endpoints

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "User Name"
}
```

**Response:**
- 201 Created: User successfully registered with JWT token
- 400 Bad Request: Invalid registration data
- 409 Conflict: Email already exists

#### POST /auth/login
Authenticate a user and return JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response:**
- 200 OK: Authentication successful with JWT token
- 401 Unauthorized: Invalid credentials

#### POST /auth/logout
Log out the current user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
- 200 OK: Successfully logged out
- 401 Unauthorized: Invalid token

### Task Management Endpoints

#### GET /api/{user_id}/tasks
Retrieve all tasks for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Parameters:**
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of tasks per page (default: 10, max: 100)
- `status` (optional): Filter by completion status ("all", "completed", "pending")
- `priority` (optional): Filter by priority ("low", "medium", "high")
- `sort` (optional): Sort order ("created", "due_date", "priority")

**Response:**
- 200 OK: List of user's tasks
- 401 Unauthorized: Invalid token
- 403 Forbidden: User attempting to access another user's tasks

**Response Body:**
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "title": "Task title",
        "description": "Task description",
        "completed": false,
        "priority": "medium",
        "due_date": "2023-12-31T23:59:59Z",
        "created_at": "2023-01-01T12:00:00Z",
        "updated_at": "2023-01-01T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "total_pages": 3
    }
  }
}
```

#### POST /api/{user_id}/tasks
Create a new task for the authenticated user.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "title": "New task title",
  "description": "Task description (optional)",
  "priority": "medium", // "low", "medium", "high"
  "due_date": "2023-12-31T23:59:59Z" // ISO 8601 format (optional)
}
```

**Response:**
- 201 Created: Task successfully created
- 400 Bad Request: Invalid task data
- 401 Unauthorized: Invalid token

**Response Body:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "New task title",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "due_date": "2023-12-31T23:59:59Z",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z",
    "user_id": 123
  }
}
```

#### GET /api/{user_id}/tasks/{id}
Retrieve a specific task by ID.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
- 200 OK: Task details
- 401 Unauthorized: Invalid token
- 403 Forbidden: User attempting to access another user's task
- 404 Not Found: Task does not exist

**Response Body:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "due_date": "2023-12-31T23:59:59Z",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z",
    "user_id": 123
  }
}
```

#### PUT /api/{user_id}/tasks/{id}
Update a specific task by ID.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "priority": "high",
  "due_date": "2023-12-31T23:59:59Z",
  "completed": true
}
```

**Response:**
- 200 OK: Task successfully updated
- 400 Bad Request: Invalid task data
- 401 Unauthorized: Invalid token
- 403 Forbidden: User attempting to update another user's task
- 404 Not Found: Task does not exist

**Response Body:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true,
    "priority": "high",
    "due_date": "2023-12-31T23:59:59Z",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-02T15:30:00Z",
    "user_id": 123
  }
}
```

#### PATCH /api/{user_id}/tasks/{id}/complete
Toggle the completion status of a specific task.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "completed": true // or false to toggle status
}
```

**Response:**
- 200 OK: Task completion status updated
- 401 Unauthorized: Invalid token
- 403 Forbidden: User attempting to update another user's task
- 404 Not Found: Task does not exist

**Response Body:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "completed": true,
    "updated_at": "2023-01-02T15:30:00Z"
  }
}
```

#### DELETE /api/{user_id}/tasks/{id}
Delete a specific task by ID.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
- 200 OK: Task successfully deleted
- 401 Unauthorized: Invalid token
- 403 Forbidden: User attempting to delete another user's task
- 404 Not Found: Task does not exist

**Response Body:**
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```

## Error Handling

### Common Error Codes
- 400 Bad Request: Invalid request data or parameters
- 401 Unauthorized: Missing or invalid authentication token
- 403 Forbidden: Insufficient permissions (e.g., accessing another user's data)
- 404 Not Found: Requested resource does not exist
- 409 Conflict: Request conflicts with current state (e.g., duplicate email)
- 422 Unprocessable Entity: Validation errors in request data
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Unexpected server error

### Rate Limiting
- Authentication endpoints: 5 attempts per minute per IP
- API endpoints: 100 requests per minute per user

## Cross-Spec References

- Authentication requirements are detailed in @specs/features/authentication.md
- Task CRUD operations are specified in @specs/features/task-crud.md
- Database schema is defined in @specs/database/schema.md