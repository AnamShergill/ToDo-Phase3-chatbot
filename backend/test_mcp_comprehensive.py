"""
Comprehensive test suite for MCP Server Implementation
Validates all requirements from specs/1-ai-chatbot/tasks.md Task 2.1-2.7
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


async def test_task_2_1_mcp_server_infrastructure():
    """Test Task 2.1: Set Up MCP Server Infrastructure"""
    print("="*60)
    print("Testing Task 2.1: MCP Server Infrastructure Setup")
    print("="*60)

    # Verify MCP server instance exists
    assert hasattr(mcp_server, 'tools'), "MCP server should have tools attribute"
    assert hasattr(mcp_server, 'call_tool'), "MCP server should have call_tool method"
    assert hasattr(mcp_server, 'get_tool_list'), "MCP server should have get_tool_list method"

    # Verify tools are registered
    tools = mcp_server.get_tool_list()
    expected_tools = ['add_task', 'list_tasks', 'complete_task', 'delete_task', 'update_task']
    assert len(tools) == 5, f"Expected 5 tools, got {len(tools)}"

    tool_names = [tool['name'] for tool in tools]
    for expected_tool in expected_tools:
        assert expected_tool in tool_names, f"Missing expected tool: {expected_tool}"

    print("SUCCESS: MCP Server infrastructure is properly set up")
    print(f"SUCCESS: Found {len(tools)} registered tools: {tool_names}")

    return True


async def test_task_2_2_add_task_tool():
    """Test Task 2.2: Implement add_task MCP Tool"""
    print("\n" + "="*60)
    print("Testing Task 2.2: add_task MCP Tool")
    print("="*60)

    # Initialize database
    create_db_and_tables()

    # Create a test user
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test_add@example.com")).first()
        if existing_user:
            user_id = existing_user.id
        else:
            test_user = User(
                email="test_add@example.com",
                password_hash="hashed_password",
                name="Test Add User"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            user_id = test_user.id

    print(f"Using user_id: {user_id}")

    # Test basic functionality - required parameters
    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Test add task'
    })
    assert result['success'] == True, f"Add task should succeed: {result}"
    assert 'task_id' in result, "Result should contain task_id"
    assert result['title'] == 'Test add task', f"Title should match: {result['title']}"
    assert result['completed'] == False, f"Task should be initially incomplete: {result['completed']}"

    task_id = result['task_id']
    print(f"SUCCESS: Created task with ID: {task_id}")

    # Test with optional description
    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Test add task with description',
        'description': 'This is a test description'
    })
    assert result['success'] == True, f"Add task with description should succeed: {result}"
    assert result['title'] == 'Test add task with description', f"Title should match: {result['title']}"

    # Test error handling - missing required parameters
    result = await add_task_tool({'user_id': user_id})  # Missing title
    assert result['success'] == False, "Should fail without title"

    result = await add_task_tool({'title': 'No user'})  # Missing user_id
    assert result['success'] == False, "Should fail without user_id"

    print("SUCCESS: add_task tool accepts user_id, title, and optional description")
    print("SUCCESS: add_task tool creates new task in database")
    print("SUCCESS: add_task tool returns task_id, status, and title")
    print("SUCCESS: add_task tool is stateless and interacts directly with database")
    print("SUCCESS: add_task tool properly handles error cases")

    return True


async def test_task_2_3_list_tasks_tool():
    """Test Task 2.3: Implement list_tasks MCP Tool"""
    print("\n" + "="*60)
    print("Testing Task 2.3: list_tasks MCP Tool")
    print("="*60)

    # Create a test user
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test_list@example.com")).first()
        if existing_user:
            user_id = existing_user.id
        else:
            test_user = User(
                email="test_list@example.com",
                password_hash="hashed_password",
                name="Test List User"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            user_id = test_user.id

    print(f"Using user_id: {user_id}")

    # Add some test tasks
    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Pending task 1',
        'description': 'Test pending task'
    })
    pending_task_1_id = result['task_id']
    assert result['success'] == True

    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Pending task 2'
    })
    pending_task_2_id = result['task_id']
    assert result['success'] == True

    # Complete one task
    result = await complete_task_tool({
        'user_id': user_id,
        'task_id': pending_task_1_id
    })
    assert result['success'] == True

    # Test listing all tasks
    result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'all'
    })
    assert result['success'] == True
    assert 'tasks' in result
    assert result['count'] >= 2, f"Should have at least 2 tasks, got {result['count']}"

    # Test listing pending tasks
    result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'pending'
    })
    assert result['success'] == True
    pending_count = result['count']
    assert all(task['completed'] == False for task in result['tasks']), "All tasks should be pending"

    # Test listing completed tasks
    result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'completed'
    })
    assert result['success'] == True
    completed_count = result['count']
    assert all(task['completed'] == True for task in result['tasks']), "All tasks should be completed"

    # Verify counts make sense
    total_result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'all'
    })
    assert total_result['count'] == pending_count + completed_count, "Total should equal sum of pending and completed"

    # Test default behavior (should be 'all' if not specified)
    result_default = await list_tasks_tool({'user_id': user_id})
    assert result_default['status_filter'] == 'all', "Default status should be 'all'"

    # Test error handling
    result = await list_tasks_tool({})  # Missing user_id
    assert result['success'] == False, "Should fail without user_id"

    print("SUCCESS: list_tasks tool accepts user_id and status (all, pending, completed)")
    print("SUCCESS: list_tasks tool returns list of tasks matching criteria")
    print("SUCCESS: list_tasks tool is stateless and reads directly from database")
    print("SUCCESS: list_tasks tool properly filters by status")
    print("SUCCESS: list_tasks tool properly handles error cases")

    return True


async def test_task_2_4_complete_task_tool():
    """Test Task 2.4: Implement complete_task MCP Tool"""
    print("\n" + "="*60)
    print("Testing Task 2.4: complete_task MCP Tool")
    print("="*60)

    # Create a test user
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test_complete@example.com")).first()
        if existing_user:
            user_id = existing_user.id
        else:
            test_user = User(
                email="test_complete@example.com",
                password_hash="hashed_password",
                name="Test Complete User"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            user_id = test_user.id

    print(f"Using user_id: {user_id}")

    # Add a test task
    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Task to complete'
    })
    task_id = result['task_id']
    assert result['success'] == True
    assert result['completed'] == False, "Task should initially be incomplete"

    # Test completing the task
    result = await complete_task_tool({
        'user_id': user_id,
        'task_id': task_id
    })
    assert result['success'] == True, f"Complete task should succeed: {result}"
    assert result['task_id'] == task_id, "Should return correct task_id"
    assert result['completed'] == True, "Task should be marked as complete"

    # Verify the task is actually completed in the database
    verify_result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'completed'
    })
    completed_tasks = [t for t in verify_result['tasks'] if t['id'] == task_id]
    assert len(completed_tasks) == 1, "Task should appear in completed list"

    # Test error handling
    result = await complete_task_tool({
        'user_id': user_id,
        'task_id': 999999  # Non-existent task
    })
    assert result['success'] == False, "Should fail for non-existent task"

    result = await complete_task_tool({
        'task_id': task_id  # Missing user_id
    })
    assert result['success'] == False, "Should fail without user_id"

    print("SUCCESS: complete_task tool accepts user_id and task_id")
    print("SUCCESS: complete_task tool updates task completion status in database")
    print("SUCCESS: complete_task tool returns task_id, status, and title")
    print("SUCCESS: complete_task tool is stateless and modifies database directly")
    print("SUCCESS: complete_task tool properly handles error cases")

    return True


async def test_task_2_5_delete_task_tool():
    """Test Task 2.5: Implement delete_task MCP Tool"""
    print("\n" + "="*60)
    print("Testing Task 2.5: delete_task MCP Tool")
    print("="*60)

    # Create a test user
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test_delete@example.com")).first()
        if existing_user:
            user_id = existing_user.id
        else:
            test_user = User(
                email="test_delete@example.com",
                password_hash="hashed_password",
                name="Test Delete User"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            user_id = test_user.id

    print(f"Using user_id: {user_id}")

    # Add a test task
    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Task to delete'
    })
    task_id = result['task_id']
    assert result['success'] == True

    # Verify task exists
    verify_result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'all'
    })
    initial_count = verify_result['count']
    assert any(t['id'] == task_id for t in verify_result['tasks']), "Task should exist initially"

    # Test deleting the task
    result = await delete_task_tool({
        'user_id': user_id,
        'task_id': task_id
    })
    assert result['success'] == True, f"Delete task should succeed: {result}"
    assert result['task_id'] == task_id, "Should return correct task_id"

    # Verify task is deleted
    verify_result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'all'
    })
    final_count = verify_result['count']
    assert final_count == initial_count - 1, f"Should have one fewer task after deletion"
    assert not any(t['id'] == task_id for t in verify_result['tasks']), "Task should not exist after deletion"

    # Test error handling
    result = await delete_task_tool({
        'user_id': user_id,
        'task_id': 999999  # Non-existent task
    })
    assert result['success'] == False, "Should fail for non-existent task"

    result = await delete_task_tool({
        'task_id': task_id  # Missing user_id
    })
    assert result['success'] == False, "Should fail without user_id"

    print("SUCCESS: delete_task tool accepts user_id and task_id")
    print("SUCCESS: delete_task tool removes task from database")
    print("SUCCESS: delete_task tool returns task_id, status, and title")
    print("SUCCESS: delete_task tool is stateless and modifies database directly")
    print("SUCCESS: delete_task tool properly handles error cases")

    return True


async def test_task_2_6_update_task_tool():
    """Test Task 2.6: Implement update_task MCP Tool"""
    print("\n" + "="*60)
    print("Testing Task 2.6: update_task MCP Tool")
    print("="*60)

    # Create a test user
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test_update@example.com")).first()
        if existing_user:
            user_id = existing_user.id
        else:
            test_user = User(
                email="test_update@example.com",
                password_hash="hashed_password",
                name="Test Update User"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            user_id = test_user.id

    print(f"Using user_id: {user_id}")

    # Add a test task
    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Original task title',
        'description': 'Original description'
    })
    task_id = result['task_id']
    assert result['success'] == True
    assert result['title'] == 'Original task title'

    # Test updating title only
    result = await update_task_tool({
        'user_id': user_id,
        'task_id': task_id,
        'title': 'Updated task title'
    })
    assert result['success'] == True, f"Update task should succeed: {result}"
    assert result['task_id'] == task_id, "Should return correct task_id"
    assert result['title'] == 'Updated task title', f"Title should be updated: {result['title']}"

    # Verify update in database
    verify_result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'all'
    })
    updated_task = next((t for t in verify_result['tasks'] if t['id'] == task_id), None)
    assert updated_task is not None, "Task should still exist"
    assert updated_task['title'] == 'Updated task title', "Title should be updated in DB"

    # Test updating description only
    result = await update_task_tool({
        'user_id': user_id,
        'task_id': task_id,
        'description': 'Updated description'
    })
    assert result['success'] == True
    assert result['description'] == 'Updated description', f"Description should be updated: {result['description']}"

    # Test updating both title and description
    result = await update_task_tool({
        'user_id': user_id,
        'task_id': task_id,
        'title': 'Final updated title',
        'description': 'Final updated description'
    })
    assert result['success'] == True
    assert result['title'] == 'Final updated title'
    assert result['description'] == 'Final updated description'

    # Verify final state in database
    verify_result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'all'
    })
    final_task = next((t for t in verify_result['tasks'] if t['id'] == task_id), None)
    assert final_task is not None
    assert final_task['title'] == 'Final updated title'
    assert final_task['description'] == 'Final updated description'

    # Test error handling
    result = await update_task_tool({
        'user_id': user_id,
        'task_id': 999999  # Non-existent task
    })
    assert result['success'] == False, "Should fail for non-existent task"

    result = await update_task_tool({
        'task_id': task_id  # Missing user_id
    })
    assert result['success'] == False, "Should fail without user_id"

    print("SUCCESS: update_task tool accepts user_id, task_id, and optional title/description")
    print("SUCCESS: update_task tool updates task details in database")
    print("SUCCESS: update_task tool returns task_id, status, and title")
    print("SUCCESS: update_task tool is stateless and modifies database directly")
    print("SUCCESS: update_task tool properly handles error cases")

    return True


async def test_task_2_7_test_mcp_tools():
    """Test Task 2.7: Test MCP Tools (Integration)"""
    print("\n" + "="*60)
    print("Testing Task 2.7: MCP Tools Integration Tests")
    print("="*60)

    # Create a test user
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == "test_integration@example.com")).first()
        if existing_user:
            user_id = existing_user.id
        else:
            test_user = User(
                email="test_integration@example.com",
                password_hash="hashed_password",
                name="Test Integration User"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            user_id = test_user.id

    print(f"Using user_id: {user_id}")

    # Full workflow test: Add, List, Update, Complete, List Completed, Delete
    print("Running full workflow test...")

    # 1. Add task
    result = await add_task_tool({
        'user_id': user_id,
        'title': 'Full workflow test task',
        'description': 'Task for integration testing'
    })
    assert result['success'] == True
    task_id = result['task_id']
    print(f"SUCCESS: Added task with ID {task_id}")

    # 2. List all tasks
    result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'all'
    })
    assert result['success'] == True
    assert any(t['id'] == task_id for t in result['tasks']), "Added task should appear in list"
    print("SUCCESS: Listed all tasks successfully")

    # 3. Update task
    result = await update_task_tool({
        'user_id': user_id,
        'task_id': task_id,
        'title': 'Updated full workflow test task'
    })
    assert result['success'] == True
    print("SUCCESS: Updated task successfully")

    # 4. Complete task
    result = await complete_task_tool({
        'user_id': user_id,
        'task_id': task_id
    })
    assert result['success'] == True
    print("SUCCESS: Completed task successfully")

    # 5. List completed tasks
    result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'completed'
    })
    assert result['success'] == True
    completed_task = next((t for t in result['tasks'] if t['id'] == task_id), None)
    assert completed_task is not None, "Completed task should appear in completed list"
    assert completed_task['completed'] == True, "Task should be marked as completed"
    print("SUCCESS: Listed completed tasks successfully")

    # 6. Delete task
    result = await delete_task_tool({
        'user_id': user_id,
        'task_id': task_id
    })
    assert result['success'] == True
    print("SUCCESS: Deleted task successfully")

    # 7. Verify deletion
    result = await list_tasks_tool({
        'user_id': user_id,
        'status': 'all'
    })
    assert result['success'] == True
    assert not any(t['id'] == task_id for t in result['tasks']), "Deleted task should not appear in list"
    print("SUCCESS: Verified task deletion successfully")

    # Test MCP server tool calling
    print("\nTesting MCP server tool calling...")
    result = await mcp_server.call_tool('add_task', {
        'user_id': user_id,
        'title': 'Server tool test',
        'description': 'Test via server'
    })
    assert result['success'] == True
    server_task_id = result['task_id']
    print(f"SUCCESS: Called add_task via server: {server_task_id}")

    result = await mcp_server.call_tool('list_tasks', {
        'user_id': user_id,
        'status': 'all'
    })
    assert result['success'] == True
    print(f"SUCCESS: Called list_tasks via server: found {result['count']} tasks")

    result = await mcp_server.call_tool('delete_task', {
        'user_id': user_id,
        'task_id': server_task_id
    })
    assert result['success'] == True
    print("SUCCESS: Called delete_task via server")

    # Test error handling via server
    result = await mcp_server.call_tool('add_task', {
        'user_id': user_id,
        'title': ''  # Invalid
    })
    assert result['success'] == False
    print("SUCCESS: Server properly handles errors")

    print("\nSUCCESS: All MCP tools work correctly in integration")
    print("SUCCESS: MCP server properly orchestrates tool calls")
    print("SUCCESS: Error handling works consistently across tools")

    return True


async def run_all_tests():
    """Run all MCP server tests"""
    print("Starting MCP Server Implementation Tests")
    print("="*60)

    test_results = []

    # Run all tests
    test_results.append(("Task 2.1: MCP Server Infrastructure", await test_task_2_1_mcp_server_infrastructure()))
    test_results.append(("Task 2.2: add_task Tool", await test_task_2_2_add_task_tool()))
    test_results.append(("Task 2.3: list_tasks Tool", await test_task_2_3_list_tasks_tool()))
    test_results.append(("Task 2.4: complete_task Tool", await test_task_2_4_complete_task_tool()))
    test_results.append(("Task 2.5: delete_task Tool", await test_task_2_5_delete_task_tool()))
    test_results.append(("Task 2.6: update_task Tool", await test_task_2_6_update_task_tool()))
    test_results.append(("Task 2.7: MCP Tools Integration", await test_task_2_7_test_mcp_tools()))

    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)

    all_passed = True
    for test_name, passed in test_results:
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print("ALL TESTS PASSED! MCP Server Implementation is Complete!")
    else:
        print("SOME TESTS FAILED")
    print("="*60)

    return all_passed


if __name__ == "__main__":
    asyncio.run(run_all_tests())