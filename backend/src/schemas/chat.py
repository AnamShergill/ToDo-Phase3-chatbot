"""
Chat API Schemas
Define request and response schemas for chat endpoint
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request schema for chat endpoint
    Accepts message and optional conversation_id
    """
    message: str
    conversation_id: Optional[str] = None


class ToolCall(BaseModel):
    """
    Schema for representing tool calls made during chat
    """
    name: str
    parameters: Dict[str, Any]


class ChatResponse(BaseModel):
    """
    Response schema for chat endpoint
    Returns conversation_id, response, and tool_calls
    """
    conversation_id: str
    response: str
    tool_calls: List[ToolCall]
    timestamp: datetime