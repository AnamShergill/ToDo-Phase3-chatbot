from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
from src.api.chat import router as chat_router
from src.database.init_db import create_db_and_tables
from src.models.user_task_models import User, Task  # Import models to register them
from src.models.conversation import Conversation  # Import to register with SQLModel
from src.models.message import Message  # Import to register with SQLModel
from contextlib import asynccontextmanager
from src.database.session import engine
from sqlmodel import SQLModel
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Create database tables on startup
        create_db_and_tables()
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        # Continue without failing the startup
    yield
    # Cleanup on shutdown if needed


app = FastAPI(
    title="TodoBoom API",
    description="API for exploding productivity in the TodoBoom application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
        "https://to-do-phase3-chatbot.vercel.app/"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}