#!/usr/bin/env python3
"""
Simple test to verify the chat API implementation without OpenAI
Tests the simulated agent functionality
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

async def test_mcp_tools_only():
    """Test MCP tools directly without OpenAI"""
    print("Testing MCP Tools Directly...")

    # Set environment variable to simulate missing OpenAI key
    os.environ["OPENAI_API_KEY"] = ""  # Empty to trigger simulated agent

    # Test user_id (we'll create a test user if needed)
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

        # Test delete_task tool
        print("\n4. Testing delete_task tool:")
        delete_result = await mcp_server.call_tool('delete_task', {
            'user_id': test_user_id,
            'task_id': task_id
        })
        print(f"   Delete result: {delete_result}")

def test_without_openai():
    """Test the service when OpenAI is not available (simulated agent)"""
    print("\n\nTesting Chat Service with Simulated Agent...")

    # Clear the OPENAI_API_KEY to trigger simulated agent
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]

    service = ChatService()  # This should initialize with simulated agent

    print(f"   Agent service type: {type(service.agent_service)}")

    # The service should now use the simulated agent
    print("   Successfully initialized chat service with simulated agent")

if __name__ == "__main__":
    print("Starting Chat API Integration Tests (without OpenAI)")
    print("=" * 60)

    # Test MCP tools directly
    asyncio.run(test_mcp_tools_only())

    # Test service without OpenAI
    test_without_openai()

    print("\n" + "=" * 60)
    print("Basic integration tests completed!")
    print("Note: Full OpenAI integration requires an API key in environment variables.")