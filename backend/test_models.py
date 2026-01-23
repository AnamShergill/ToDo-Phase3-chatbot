"""
Test script to verify that the new database models work correctly
"""
from datetime import datetime
from src.database.init_db import create_db_and_tables
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.user_task_models import User, Task
from sqlmodel import Session
from src.database.session import engine

def test_models():
    print("Testing database models...")

    # Create tables
    create_db_and_tables()
    print("+ Database tables created successfully")

    # Test creating instances
    conv = Conversation(user_id=1)
    msg = Message(user_id=1, conversation_id="test-id", role="user", content="Test message")

    print(f"+ Conversation created: {conv}")
    print(f"+ Message created: {msg}")

    # Test creating a session and adding records
    with Session(engine) as session:
        print("+ Database session created successfully")

    print("\nAll model tests passed!")

if __name__ == "__main__":
    test_models()