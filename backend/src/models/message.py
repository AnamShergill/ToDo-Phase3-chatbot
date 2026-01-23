from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .user_task_models import User  # Forward reference for type checking
    from .conversation import Conversation  # Forward reference for type checking


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    conversation_id: str = Field(foreign_key="conversations.id", nullable=False)
    role: str = Field(nullable=False)  # "user" or "assistant"
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship()
    conversation: "Conversation" = Relationship(back_populates="messages")