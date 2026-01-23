# Database Schema Specification

## Overview

The Todo application uses Neon Serverless PostgreSQL as its primary database. The schema implements proper data isolation between users and follows security best practices for storing sensitive information.

## Database Tables

### Users Table

Stores user account information and authentication data.

**Table Name:** `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the user |
| email | VARCHAR(255) | NOT NULL, UNIQUE | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | BCrypt hash of user's password |
| name | VARCHAR(255) | NOT NULL | User's display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes:**
- `idx_users_email`: UNIQUE INDEX on email column for fast lookups and uniqueness enforcement

**Foreign Key Constraints:** None

### Tasks Table

Stores task information associated with each user.

**Table Name:** `tasks`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the task |
| user_id | INTEGER | NOT NULL, FOREIGN KEY | Reference to the user who owns the task |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULL | Optional task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| priority | VARCHAR(20) | NOT NULL, DEFAULT 'medium' | Task priority ('low', 'medium', 'high') |
| due_date | TIMESTAMP | NULL | Optional due date for the task |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Task creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes:**
- `idx_tasks_user_id`: INDEX on user_id column for efficient user-based queries
- `idx_tasks_completed`: INDEX on completed column for filtering by status
- `idx_tasks_priority`: INDEX on priority column for priority-based queries
- `idx_tasks_due_date`: INDEX on due_date column for due date filtering
- `idx_tasks_user_completed`: COMPOSITE INDEX on (user_id, completed) for efficient user task queries

**Foreign Key Constraints:**
- `fk_tasks_user_id`: REFERENCES users(id) with CASCADE on DELETE and UPDATE

## Data Integrity Rules

### Users Table
1. Email must be unique across all users
2. Email must follow standard email format validation
3. Password must be stored as a secure hash (not plain text)
4. Name cannot be empty

### Tasks Table
1. Each task must be associated with a valid user
2. Title cannot be empty
3. Priority must be one of 'low', 'medium', or 'high'
4. Completed status defaults to false
5. Tasks are automatically assigned creation timestamp
6. Tasks are automatically updated with modification timestamp

## Security Considerations

### Data Encryption
- Passwords are stored as bcrypt hashes with salt
- Sensitive data is not stored in plain text
- Database connections use SSL encryption

### Access Control
- User data is isolated by user_id foreign key relationships
- Authentication is required before accessing any user data
- Database queries always filter by authenticated user

### Indexing Strategy
- Primary indexes on all ID columns for fast lookups
- Foreign key columns are indexed for join performance
- Frequently queried columns (completed, priority) are indexed
- Composite indexes for common query patterns

## Database Constraints

### Referential Integrity
- Tasks table has foreign key relationship to users table
- CASCADE DELETE ensures tasks are removed when user is deleted
- CASCADE UPDATE ensures foreign key references update with user ID changes

### Check Constraints
- Tasks priority must be one of the allowed values: 'low', 'medium', 'high'
- Due date must be a valid timestamp or NULL
- Title must not be empty

## Performance Considerations

### Query Optimization
- Indexes on user_id to optimize user-specific queries
- Composite index for common filtering scenarios (user_id, completed)
- Proper indexing for sorting operations (due_date, priority)

### Scalability
- UUIDs could be considered for future horizontal scaling
- Partitioning strategy available for large datasets
- Connection pooling handled at application level

## Cross-Spec References

- User authentication requirements are detailed in @specs/features/authentication.md
- Task CRUD operations are specified in @specs/features/task-crud.md
- API endpoints that interact with the database are documented in @specs/api/rest-endpoints.md