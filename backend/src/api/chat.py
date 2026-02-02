"""
Chat API Endpoint
POST /api/{user_id}/chat endpoint for handling chat requests
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from src.services.chat_service import ChatService
from src.schemas.chat import ChatRequest, ChatResponse
from src.middleware.auth import verify_token


router = APIRouter(prefix="/api/{user_id}")


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: int,
    chat_request: ChatRequest,
    authenticated_user_id: int = Depends(verify_token)
) -> ChatResponse:
    """
    POST endpoint at /api/{user_id}/chat
    - Stateless operation loading full conversation history
    - Integration with OpenAI Agent and MCP tools
    - Proper response formatting
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(authenticated_user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to access this user's chat")

    try:
        # Create chat service instance
        chat_service = ChatService()

        # Process the chat request
        result = await chat_service.process_chat_request(
            user_id=user_id,
            message=chat_request.message,
            conversation_id=chat_request.conversation_id
        )

        # Return the response
        return ChatResponse(
            conversation_id=result['conversation_id'],
            response=result['response'],
            tool_calls=result['tool_calls'],
            timestamp=result['timestamp']
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


# Include a simple test endpoint for debugging
@router.get("/chat/test")
async def test_chat_endpoint(user_id: int, authenticated_user_id: int = Depends(verify_token)):
    """
    Simple test endpoint to verify the chat API is working
    """
    if str(authenticated_user_id) != str(user_id):
        raise HTTPException(status_code=403, detail="Not authorized to access this user's chat")

    return {"message": f"Chat API is working for user {user_id}"}