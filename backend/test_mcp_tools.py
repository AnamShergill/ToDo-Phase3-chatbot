"""
Test suite for MCP tools
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mcp.server import mcp_server
from src.mcp.tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool
from src.database.init_db import create_db_and_tables
from sqlmodel import Session, select
from src.models.user_task_models import User, Task
from src.database.session import engine


async def test_mcp_tools():
    print("Testing MCP Tools...")

    # Initialize database
    create_db_and_tables()

    # Create a test user
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
        if existing_user:
            user_id = existing_user.id
        else:
            test_user = User(
                email="test@example.com",
                password_hash="hashed_password",
                name="Test User"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            user_id = test_user.id

    print(f"Using user_id: {user_id}")

    # Test add_task tool
    print("\n1. Testing add_task tool...")
    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Test task from MCP',
        'description': 'This is a test task created via MCP tool'
    })
    print(f"Add task result: {result}")

    if result['success']:
        task_id = result['task_id']

        # Test list_tasks tool
        print("\n2. Testing list_tasks tool...")
        result = await list_tasks_tool({
            'user_id': user_id,
            'status': 'all'
        })
        print(f"List tasks result: {result}")

        # Test update_task tool
        print("\n3. Testing update_task tool...")
        result = await update_task_tool({
            'user_id': user_id,
            'task_id': task_id,
            'title': 'Updated test task from MCP',
            'description': 'This is an updated test task created via MCP tool'
        })
        print(f"Update task result: {result}")

        # Test complete_task tool
        print("\n4. Testing complete_task tool...")
        result = await complete_task_tool({
            'user_id': user_id,
            'task_id': task_id
        })
        print(f"Complete task result: {result}")

        # Test list_tasks again to see completed task
        print("\n5. Testing list_tasks tool after completion...")
        result = await list_tasks_tool({
            'user_id': user_id,
            'status': 'completed'
        })
        print(f"List completed tasks result: {result}")

        # Test delete_task tool
        print("\n6. Testing delete_task tool...")
        result = await delete_task_tool({
            'user_id': user_id,
            'task_id': task_id
        })
        print(f"Delete task result: {result}")

    # Test error cases
    print("\n7. Testing error cases...")
    result = await add_task_tool({
        'user_id': user_id,
        'title': ''  # Invalid title
    })
    print(f"Invalid input result: {result}")

    result = await complete_task_tool({
        'user_id': user_id,
        'task_id': 999999  # Non-existent task
    })
    print(f"Non-existent task result: {result}")

    # Test server tool calling
    print("\n8. Testing MCP server tool calling...")
    result = await mcp_server.call_tool('list_tasks', {
        'user_id': user_id,
        'status': 'all'
    })
    print(f"Server call result: {result}")

    # Test get tool list
    print("\n9. Testing get tool list...")
    tools = mcp_server.get_tool_list()
    print(f"Available tools: {len(tools)}")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")

    print("\nMCP Tools testing completed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_tools())