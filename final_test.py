#!/usr/bin/env python3
"""
Final comprehensive test to verify the TodoBoom AI Chatbot is fully functional
"""

import asyncio
import sys
import os

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_core_components():
    """Test that all core components can be imported and instantiated"""
    print("=" * 60)
    print("TESTING CORE COMPONENTS")
    print("=" * 60)

    success_count = 0
    total_tests = 0

    # Test MCP Server
    total_tests += 1
    try:
        from mcp.server import mcp_server
        print(f"✓ MCP Server: {len(mcp_server.tools)} tools registered")
        print(f"  Tools: {list(mcp_server.tools.keys())}")
        success_count += 1
    except Exception as e:
        print(f"✗ MCP Server: {e}")

    # Test MCP Tools
    total_tests += 1
    try:
        from mcp.tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool
        print("✓ MCP Tools: All 5 tools imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ MCP Tools: {e}")

    # Test Services
    total_tests += 1
    try:
        from services.chat_service import ChatService
        from services.conversation_service import ConversationService
        print("✓ Services: Chat and Conversation services imported")
        success_count += 1
    except Exception as e:
        print(f"✗ Services: {e}")

    # Test API Router
    total_tests += 1
    try:
        from api.chat import router
        print("✓ API: Chat router imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ API: {e}")

    # Test Models
    total_tests += 1
    try:
        from models.conversation import Conversation
        from models.message import Message
        from models.user_task_models import Task
        print("✓ Models: All models imported successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ Models: {e}")

    print(f"\nCore Components: {success_count}/{total_tests} tests passed")
    return success_count == total_tests

async def test_mcp_functionality():
    """Test MCP tools functionality"""
    print("\n" + "=" * 60)
    print("TESTING MCP TOOLS FUNCTIONALITY")
    print("=" * 60)

    success_count = 0
    total_tests = 0

    # Import tools
    from mcp.tools import add_task_tool, list_tasks_tool, complete_task_tool, delete_task_tool, update_task_tool

    # Test 1: Add a task
    total_tests += 1
    try:
        params = {
            'user_id': 1,
            'title': 'Test task for functionality verification',
            'description': 'This is a test task created during functionality verification'
        }
        result = await add_task_tool(params)
        if result['success'] and result['task_id']:
            task_id = result['task_id']
            print(f"✓ Add Task: Created task #{task_id}")
            success_count += 1
        else:
            print(f"✗ Add Task: Failed - {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Add Task: Exception - {e}")

    # Test 2: List tasks
    total_tests += 1
    if success_count >= 1:  # Only run if add task succeeded
        try:
            params = {'user_id': 1, 'status': 'all'}
            result = await list_tasks_tool(params)
            if result['success']:
                print(f"✓ List Tasks: Found {result['count']} tasks, status filter: {result['status_filter']}")
                success_count += 1
            else:
                print(f"✗ List Tasks: Failed - {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"✗ List Tasks: Exception - {e}")

    # Test 3: Update task (if we have a task ID)
    total_tests += 1
    if success_count >= 2 and 'task_id' in locals():
        try:
            params = {
                'user_id': 1,
                'task_id': task_id,
                'title': 'Updated test task for functionality verification'
            }
            result = await update_task_tool(params)
            if result['success']:
                print(f"✓ Update Task: Updated task #{task_id}")
                success_count += 1
            else:
                print(f"✗ Update Task: Failed - {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"✗ Update Task: Exception - {e}")

    # Test 4: Complete task
    total_tests += 1
    if success_count >= 3 and 'task_id' in locals():
        try:
            params = {'user_id': 1, 'task_id': task_id}
            result = await complete_task_tool(params)
            if result['success']:
                print(f"✓ Complete Task: Completed task #{task_id}")
                success_count += 1
            else:
                print(f"✗ Complete Task: Failed - {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"✗ Complete Task: Exception - {e}")

    # Test 5: Delete task
    total_tests += 1
    if success_count >= 4 and 'task_id' in locals():
        try:
            params = {'user_id': 1, 'task_id': task_id}
            result = await delete_task_tool(params)
            if result['success']:
                print(f"✓ Delete Task: Deleted task #{task_id}")
                success_count += 1
            else:
                print(f"✗ Delete Task: Failed - {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"✗ Delete Task: Exception - {e}")

    print(f"\nMCP Functionality: {success_count}/{total_tests} tests passed")
    return success_count == total_tests

async def test_chat_service():
    """Test chat service functionality"""
    print("\n" + "=" * 60)
    print("TESTING CHAT SERVICE")
    print("=" * 60)

    success_count = 0
    total_tests = 0

    total_tests += 1
    try:
        from services.chat_service import ChatService
        chat_service = ChatService()
        print("✓ Chat Service: Instantiated successfully")
        print(f"  Agent available: {chat_service.agent_service is not None}")
        if chat_service.agent_service is None:
            print("  Using simulated agent (no OpenAI API key found)")
        success_count += 1
    except Exception as e:
        print(f"✗ Chat Service: {e}")

    # Test conversation service
    total_tests += 1
    try:
        from services.conversation_service import ConversationService
        conv_service = ConversationService()
        print("✓ Conversation Service: Instantiated successfully")
        success_count += 1
    except Exception as e:
        print(f"✗ Conversation Service: {e}")

    print(f"\nChat Service: {success_count}/{total_tests} tests passed")
    return success_count == total_tests

async def main():
    """Run all tests"""
    print("TODOBOOM AI CHATBOT - COMPREHENSIVE FUNCTIONALITY TEST")
    print("=" * 60)

    # Run all tests
    core_ok = test_core_components()
    mcp_ok = await test_mcp_functionality()
    chat_ok = await test_chat_service()

    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)

    print(f"Core Components: {'PASS' if core_ok else 'FAIL'}")
    print(f"MCP Functionality: {'PASS' if mcp_ok else 'FAIL'}")
    print(f"Chat Service: {'PASS' if chat_ok else 'FAIL'}")

    overall_success = core_ok and mcp_ok and chat_ok
    print(f"\nOVERALL STATUS: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")

    if overall_success:
        print("\n🎉 TODOBOOM AI CHATBOT IS FULLY FUNCTIONAL! 🎉")
        print("All components are working correctly and integrated properly.")
    else:
        print("\n⚠️  Some components may need attention.")

    return overall_success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)