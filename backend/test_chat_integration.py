#!/usr/bin/env python3
"""
Test script to verify the chat API implementation
Tests the full integration of OpenAI Agent + MCP tools + Chat API
"""

import asyncio
import os
from src.services.chat_service import ChatService
from src.services.conversation_service import ConversationService
from src.mcp.server import mcp_server
from src.models.user_task_models import User, Task
from src.database.session import engine
from sqlmodel import Session, select
from datetime import datetime

async def test_mcp_tools():
    """Test all MCP tools directly"""
    print("Testing MCP Tools...")

    # Test user_id (using 1 as a test user)
    test_user_id = 1

    # Test add_task tool
    print("\n1. Testing add_task tool:")
    add_result = await mcp_server.call_tool('add_task', {
        'user_id': test_user_id,
        'title': 'Test task from integration test',
        'description': 'This is a test task created by the integration test'
    })
    print(f"   Add result: {add_result}")

    if add_result.get('success'):
        task_id = add_result['task_id']

        # Test list_tasks tool
        print("\n2. Testing list_tasks tool:")
        list_result = await mcp_server.call_tool('list_tasks', {
            'user_id': test_user_id,
            'status': 'all'
        })
        print(f"   List result: {list_result}")

        # Test complete_task tool
        print("\n3. Testing complete_task tool:")
        complete_result = await mcp_server.call_tool('complete_task', {
            'user_id': test_user_id,
            'task_id': task_id
        })
        print(f"   Complete result: {complete_result}")

        # Test update_task tool
        print("\n4. Testing update_task tool:")
        update_result = await mcp_server.call_tool('update_task', {
            'user_id': test_user_id,
            'task_id': task_id,
            'title': 'Updated test task',
            'description': 'Updated description'
        })
        print(f"   Update result: {update_result}")

        # Test delete_task tool
        print("\n5. Testing delete_task tool:")
        delete_result = await mcp_server.call_tool('delete_task', {
            'user_id': test_user_id,
            'task_id': task_id
        })
        print(f"   Delete result: {delete_result}")

async def test_conversation_service():
    """Test conversation service functionality"""
    print("\n\nTesting Conversation Service...")

    service = ConversationService()

    # Create a new conversation
    print("\n1. Creating new conversation:")
    conversation = service.get_or_create_conversation(user_id=1)
    print(f"   Created conversation ID: {conversation.id}")

    # Save a user message
    print("\n2. Saving user message:")
    user_msg = service.save_message(
        conversation_id=conversation.id,
        user_id=1,
        role='user',
        content='Test message from user'
    )
    print(f"   Saved user message ID: {user_msg.id}")

    # Save an assistant message
    print("\n3. Saving assistant message:")
    assistant_msg = service.save_message(
        conversation_id=conversation.id,
        user_id=1,
        role='assistant',
        content='Test response from assistant'
    )
    print(f"   Saved assistant message ID: {assistant_msg.id}")

    # Get conversation history
    print("\n4. Retrieving conversation history:")
    history = service.get_conversation_history(conversation.id, 1)
    print(f"   Retrieved {len(history)} messages:")
    for msg in history:
        print(f"     - {msg['role']}: {msg['content']}")

async def test_chat_service():
    """Test the full chat service with simulated agent"""
    print("\n\nTesting Chat Service...")

    service = ChatService()

    # Test with a message that should trigger MCP tools
    print("\n1. Testing chat with task creation:")
    result = await service.process_chat_request(
        user_id=1,
        message="Add a task to buy groceries for tomorrow",
        conversation_id=None
    )
    print(f"   Chat result: {result}")

    # Test with a message that should list tasks
    print("\n2. Testing chat with task listing:")
    result2 = await service.process_chat_request(
        user_id=1,
        message="List all my tasks",
        conversation_id=result['conversation_id']
    )
    print(f"   Chat result: {result2}")

async def main():
    print("Starting Chat API Integration Tests")
    print("=" * 50)

    # Test MCP tools
    await test_mcp_tools()

    # Test conversation service
    await test_conversation_service()

    # Test chat service
    await test_chat_service()

    print("\n" + "=" * 50)
    print("Integration tests completed!")

if __name__ == "__main__":
    asyncio.run(main())