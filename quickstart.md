# Todo App Quickstart

## Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL (or Neon account)

## Setup

1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies: `npm install`
4. Set up environment variables (see .env.example)
5. Run database migrations
6. Start backend: `uvicorn main:app --reload`
7. Start frontend: `npm run dev`

## Development
- Backend: FastAPI running on http://localhost:8000
- Frontend: Next.js running on http://localhost:3000
- API documentation: http://localhost:8000/docs