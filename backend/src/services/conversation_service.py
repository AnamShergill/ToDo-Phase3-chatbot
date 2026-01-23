"""
Conversation Management Service
Handles conversation lifecycle operations
"""

from typing import Optional
from sqlmodel import Session, select
from datetime import datetime
from uuid import UUID, uuid4
from src.models.conversation import Conversation
from src.models.message import Message
from src.database.session import engine


class ConversationService:
    """
    Service for managing conversation lifecycle
    - Creates new conversations when needed
    - Retrieves existing conversations
    - Updates conversation metadata
    - Manages timestamps
    """

    @staticmethod
    def get_or_create_conversation(user_id: int, conversation_id: Optional[str] = None) -> Conversation:
        """
        Get existing conversation or create a new one
        """
        with Session(engine) as session:
            if conversation_id:
                # Try to find existing conversation
                existing_conv = session.exec(
                    select(Conversation)
                    .where(Conversation.id == conversation_id)
                    .where(Conversation.user_id == user_id)
                ).first()

                if existing_conv:
                    # Update the conversation's updated_at timestamp
                    existing_conv.updated_at = datetime.utcnow()
                    session.add(existing_conv)
                    session.commit()
                    session.refresh(existing_conv)
                    return existing_conv

            # Create new conversation
            new_conversation = Conversation(
                user_id=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
            return new_conversation

    @staticmethod
    def get_conversation_history(conversation_id: str, user_id: int) -> list:
        """
        Load full conversation history from database
        """
        with Session(engine) as session:
            messages = session.exec(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .where(Message.user_id == user_id)
                .order_by(Message.created_at.asc())
            ).all()

            return [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.created_at.isoformat()
                }
                for msg in messages
            ]

    @staticmethod
    def save_message(conversation_id: str, user_id: int, role: str, content: str) -> Message:
        """
        Save a message to the conversation
        """
        with Session(engine) as session:
            message = Message(
                user_id=user_id,
                conversation_id=conversation_id,
                role=role,
                content=content,
                created_at=datetime.utcnow()
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message