import requests
import json
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Configuration - use the same secret as the backend
SECRET_KEY = "your-super-secret-key-change-this-in-production"  # From backend/.env
ALGORITHM = "HS256"

def create_test_token(user_id):
    """Create a test JWT token for a given user ID"""
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.utcnow()
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Test the chat API with a manually created token
BASE_URL = "http://localhost:8000"

# Create a test token for user ID 1
test_token = create_test_token(1)
headers = {
    "Authorization": f"Bearer {test_token}",
    "Content-Type": "application/json"
}

print("TODOBOOM AI CHATBOT - DELETE TASK FUNCTIONALITY TEST")
print("=" * 60)

# Test 1: Add a task first
print("\n1. Adding a test task:")
chat_data = {
    "message": "Add a task to buy groceries for dinner",
    "conversation_id": None
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Response: {result['response']}")
        print(f"   Tool Calls: {len(result['tool_calls'])}")
        if result['tool_calls']:
            for tool_call in result['tool_calls']:
                print(f"     - {tool_call['name']}: {tool_call['parameters']}")
        conversation_id = result['conversation_id']
        print(f"   Conversation ID: {conversation_id}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: List tasks to see the newly added task
print("\n2. Listing all tasks:")
chat_data = {
    "message": "Show me all my tasks",
    "conversation_id": conversation_id
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Response: {result['response'][:100]}{'...' if len(result['response']) > 100 else ''}")
        print(f"   Tool Calls: {len(result['tool_calls'])}")
        if result['tool_calls']:
            for tool_call in result['tool_calls']:
                print(f"     - {tool_call['name']}: {tool_call['parameters']}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Try to delete the task by name
print("\n3. Attempting to delete the task 'buy groceries for dinner':")
chat_data = {
    "message": "Delete the task buy groceries for dinner",
    "conversation_id": conversation_id
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Response: {result['response']}")
        print(f"   Tool Calls: {len(result['tool_calls'])}")
        if result['tool_calls']:
            for tool_call in result['tool_calls']:
                print(f"     - {tool_call['name']}: {tool_call['parameters']}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test 4: List tasks again to confirm deletion
print("\n4. Listing tasks again to confirm deletion:")
chat_data = {
    "message": "Show me all my tasks",
    "conversation_id": conversation_id
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Response: {result['response'][:100]}{'...' if len(result['response']) > 100 else ''}")
        print(f"   Tool Calls: {len(result['tool_calls'])}")
        if result['tool_calls']:
            for tool_call in result['tool_calls']:
                print(f"     - {tool_call['name']}: {tool_call['parameters']}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("DELETE TASK FUNCTIONALITY TEST COMPLETE!")
print("- Add task: Should work")
print("- List tasks: Should work")
print("- Delete task by name: Should now work with enhanced logic")
print("- Verify deletion: Should confirm task is gone")
print("=" * 60)