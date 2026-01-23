# Todo Application Data Model

## User Entity

**Entity Name**: User
**Description**: Represents a registered user in the system

### Fields
- `id`: INTEGER, PRIMARY KEY, AUTO_INCREMENT
  - Purpose: Unique identifier for the user
  - Constraints: Required, Unique, Auto-generated

- `email`: VARCHAR(255), NOT NULL
  - Purpose: User's email address for login
  - Constraints: Required, Unique, Valid email format

- `password_hash`: VARCHAR(255), NOT NULL
  - Purpose: BCrypt hash of user's password
  - Constraints: Required, Securely hashed

- `name`: VARCHAR(255), NOT NULL
  - Purpose: User's display name
  - Constraints: Required, Non-empty

- `created_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
  - Purpose: Timestamp when user account was created
  - Constraints: Automatically set on creation

- `updated_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  - Purpose: Timestamp when user account was last updated
  - Constraints: Automatically updated on changes

### Relationships
- One-to-many with Task entity (one user can have many tasks)

### Validation Rules
- Email must be unique across all users
- Email must follow standard email format validation
- Password must be stored as a secure hash (never plain text)
- Name cannot be empty

## Task Entity

**Entity Name**: Task
**Description**: Represents a task item belonging to a user

### Fields
- `id`: INTEGER, PRIMARY KEY, AUTO_INCREMENT
  - Purpose: Unique identifier for the task
  - Constraints: Required, Unique, Auto-generated

- `user_id`: INTEGER, NOT NULL, FOREIGN KEY
  - Purpose: Reference to the user who owns the task
  - Constraints: Required, Must reference valid user

- `title`: VARCHAR(255), NOT NULL
  - Purpose: Task title/description
  - Constraints: Required, Non-empty

- `description`: TEXT, NULL
  - Purpose: Detailed description of the task
  - Constraints: Optional field

- `completed`: BOOLEAN, DEFAULT FALSE
  - Purpose: Completion status of the task
  - Constraints: Required, Default to false

- `priority`: VARCHAR(20), DEFAULT 'medium'
  - Purpose: Priority level of the task
  - Constraints: Required, One of 'low', 'medium', 'high'

- `due_date`: TIMESTAMP, NULL
  - Purpose: Optional deadline for the task
  - Constraints: Optional, Valid timestamp if provided

- `created_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
  - Purpose: Timestamp when task was created
  - Constraints: Automatically set on creation

- `updated_at`: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  - Purpose: Timestamp when task was last updated
  - Constraints: Automatically updated on changes

### Relationships
- Many-to-one with User entity (many tasks belong to one user)

### Validation Rules
- Each task must be associated with a valid user
- Title cannot be empty
- Priority must be one of 'low', 'medium', or 'high'
- Completed status defaults to false
- Tasks are automatically assigned creation timestamp
- Tasks are automatically updated with modification timestamp

## State Transitions

### Task State Transitions
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user unmarks task as complete

### User State Transitions
- `registered` → `active`: When user successfully authenticates for the first time
- `active` → `inactive`: When user account is deactivated (future feature)

## Indexes

### Users Table
- `idx_users_email`: UNIQUE INDEX on email column for fast lookups and uniqueness enforcement

### Tasks Table
- `idx_tasks_user_id`: INDEX on user_id column for efficient user-based queries
- `idx_tasks_completed`: INDEX on completed column for filtering by status
- `idx_tasks_priority`: INDEX on priority column for priority-based queries
- `idx_tasks_due_date`: INDEX on due_date column for due date filtering
- `idx_tasks_user_completed`: COMPOSITE INDEX on (user_id, completed) for efficient user task queries

## Foreign Key Constraints

### Tasks Table
- `fk_tasks_user_id`: REFERENCES users(id) with CASCADE on DELETE and UPDATE
  - Ensures referential integrity between tasks and users
  - Automatically removes tasks when user is deleted
  - Automatically updates user references if user ID changes

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

## Cross-Spec References

- User authentication requirements are detailed in @specs/features/authentication.md
- Task CRUD operations are specified in @specs/features/task-crud.md
- Database schema is defined in @specs/database/schema.md