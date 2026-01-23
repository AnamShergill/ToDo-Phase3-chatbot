# TodoBoom - Full-Stack Todo Application

TodoBoom is a modern full-stack todo application built with Next.js, FastAPI, Better Auth, and Neon PostgreSQL.

<!-- Updated on $(date +%Y-%m-%d) - Changes: Removed chatbot, added welcome page, enhanced dashboard -->

## Tech Stack

- **Frontend**: Next.js 14 (App Router, TypeScript, Tailwind CSS)
- **Backend**: FastAPI (Python)
- **Authentication**: Better Auth + JWT
- **Database**: Neon PostgreSQL (with SQLModel)
- **Deployment**: Vercel (frontend), Render (backend)

## Features

- User authentication and authorization
- Create, read, update, and delete tasks
- Task filtering and sorting
- Responsive design for all devices
- JWT-based authentication with refresh tokens

## Project Structure

```
.
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # Reusable UI components
│   │   ├── context/         # React context providers
│   │   ├── lib/            # Utility functions and API clients
│   │   └── styles/         # Global styles
│   ├── public/             # Static assets
│   ├── next.config.js      # Next.js configuration
│   └── package.json
├── backend/                # FastAPI backend application
│   ├── src/
│   │   ├── api/           # API route handlers
│   │   ├── database/      # Database configuration
│   │   ├── middleware/    # Middleware functions
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic
│   ├── main.py            # Main application entry point
│   ├── requirements.txt   # Python dependencies
│   └── .env.example       # Environment variable template
├── README.md              # This file
└── CLAUDE.md              # Project instructions
```

## Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Copy the environment file and update the values:
```bash
cp .env.local.example .env.local
```

4. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the environment file and update the values:
```bash
cp .env.example .env
```

4. Start the development server:
```bash
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

## Environment Variables

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL (e.g., http://localhost:8000)
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Better Auth base URL (e.g., http://localhost:8000)

### Backend (.env)
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT signing
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time in minutes

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set the following environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_BASE_URL`: Your backend API URL
   - `NEXT_PUBLIC_BETTER_AUTH_URL`: Your backend API URL
3. Set the build command to `npm run build`
4. Set the output directory to `.next`

### Backend (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the runtime to Python
4. Set the build command to `pip install -r requirements.txt`
5. Set the start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables in Render dashboard:
   - `SECRET_KEY`: A strong random secret key
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `ALGORITHM`: Algorithm for JWT (default: HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT expiration time

Alternatively, use the provided `render.yaml` file for automated deployment.

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout

### Tasks
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task

## Security

- JWT-based authentication with expiration
- Password hashing using bcrypt
- Input validation using Pydantic
- SQL injection protection via SQLModel ORM
- CORS configured for secure cross-origin requests

## Development Guidelines

- Use consistent error handling across API endpoints
- Follow the existing code style and naming conventions
- Write tests for new functionality
- Update documentation when adding new features
- Use environment variables for configuration