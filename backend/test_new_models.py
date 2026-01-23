"""
Unit tests for the new Conversation and Message models
"""
from datetime import datetime
from src.database.init_db import create_db_and_tables
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.user_task_models import User, Task
from sqlmodel import Session, select
from src.database.session import engine
import uuid


def test_conversation_model():
    """Test Conversation model creation and attributes"""
    print("Testing Conversation model...")

    # Create a conversation instance
    conv = Conversation(user_id=1)

    # Check that required attributes are present
    assert hasattr(conv, 'id'), "Conversation should have an id"
    assert hasattr(conv, 'user_id'), "Conversation should have a user_id"
    assert hasattr(conv, 'created_at'), "Conversation should have created_at"
    assert hasattr(conv, 'updated_at'), "Conversation should have updated_at"

    # Check that id is generated
    assert conv.id is not None, "Conversation id should be generated"

    # Check that user_id is set correctly
    assert conv.user_id == 1, "Conversation user_id should be set correctly"

    print("+ Conversation model attributes are correct")


def test_message_model():
    """Test Message model creation and attributes"""
    print("Testing Message model...")

    # Create a message instance
    msg = Message(
        user_id=1,
        conversation_id=str(uuid.uuid4()),
        role="user",
        content="Test message content"
    )

    # Check that required attributes are present
    assert hasattr(msg, 'id'), "Message should have an id"
    assert hasattr(msg, 'user_id'), "Message should have a user_id"
    assert hasattr(msg, 'conversation_id'), "Message should have a conversation_id"
    assert hasattr(msg, 'role'), "Message should have a role"
    assert hasattr(msg, 'content'), "Message should have content"
    assert hasattr(msg, 'created_at'), "Message should have created_at"

    # Check that values are set correctly
    assert msg.user_id == 1, "Message user_id should be set correctly"
    assert msg.role == "user", "Message role should be set correctly"
    assert msg.content == "Test message content", "Message content should be set correctly"

    print("+ Message model attributes are correct")


def test_database_integration():
    """Test database integration with new models"""
    print("Testing database integration...")

    # Create tables
    create_db_and_tables()

    with Session(engine) as session:
        # Create a test conversation
        conv = Conversation(user_id=1)
        session.add(conv)
        session.commit()
        session.refresh(conv)

        # Verify conversation was saved
        assert conv.id is not None, "Conversation should be saved with an ID"
        assert conv.user_id == 1, "Conversation user_id should be preserved"

        # Create a test message
        msg = Message(
            user_id=1,
            conversation_id=conv.id,
            role="user",
            content="Test message for integration test"
        )
        session.add(msg)
        session.commit()
        session.refresh(msg)

        # Verify message was saved
        assert msg.id is not None, "Message should be saved with an ID"
        assert msg.conversation_id == conv.id, "Message should reference the correct conversation"

        # Test relationship by querying the conversation and its messages
        retrieved_conv = session.get(Conversation, conv.id)
        assert retrieved_conv is not None, "Conversation should be retrievable"

        print("+ Database integration tests passed")


def test_relationships():
    """Test relationships between models"""
    print("Testing model relationships...")

    with Session(engine) as session:
        # Create a conversation
        conv = Conversation(user_id=1)
        session.add(conv)
        session.commit()
        session.refresh(conv)

        # Create multiple messages for the conversation
        msg1 = Message(
            user_id=1,
            conversation_id=conv.id,
            role="user",
            content="First message"
        )
        msg2 = Message(
            user_id=1,
            conversation_id=conv.id,
            role="assistant",
            content="Assistant response"
        )

        session.add(msg1)
        session.add(msg2)
        session.commit()

        # Retrieve the conversation and check its messages
        retrieved_conv = session.get(Conversation, conv.id)
        assert retrieved_conv is not None, "Conversation should be retrievable"
        assert len(retrieved_conv.messages) >= 2, f"Conversation should have at least 2 messages, got {len(retrieved_conv.messages)}"

        # Check that messages have correct conversation reference
        for message in retrieved_conv.messages:
            assert message.conversation_id == conv.id, f"Message should reference correct conversation, got {message.conversation_id}"

        print("+ Relationship tests passed")


def run_all_tests():
    """Run all tests"""
    print("Running database model tests...\n")

    test_conversation_model()
    test_message_model()
    test_database_integration()
    test_relationships()

    print("\nAll tests passed! SUCCESS")


if __name__ == "__main__":
    run_all_tests()