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

print("TODOBOOM AI CHATBOT - SPECIFIC DELETE TEST")
print("=" * 50)

# Step 1: Add a specific task first to have something to delete
print("\n1. Adding a specific task to delete:")
chat_data = {
    "message": "Add a task to buy apples",
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

# Step 2: List tasks to confirm the new task exists
print("\n2. Listing tasks to confirm new task exists:")
chat_data = {
    "message": "list tasks",
    "conversation_id": conversation_id
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Response: {result['response'][:200]}{'...' if len(result['response']) > 200 else ''}")
        print(f"   Tool Calls: {len(result['tool_calls'])}")
        if result['tool_calls']:
            for tool_call in result['tool_calls']:
                print(f"     - {tool_call['name']}: {tool_call['parameters']}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# Step 3: Try to delete the specific task we just added
print("\n3. Attempting to delete 'buy apples' task:")
chat_data = {
    "message": "delete buy apples",
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

# Step 4: List tasks again to confirm deletion
print("\n4. Listing tasks again to confirm deletion:")
chat_data = {
    "message": "list tasks",
    "conversation_id": conversation_id
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Response: {result['response'][:200]}{'...' if len(result['response']) > 200 else ''}")
        print(f"   Tool Calls: {len(result['tool_calls'])}")
        if result['tool_calls']:
            for tool_call in result['tool_calls']:
                print(f"     - {tool_call['name']}: {tool_call['parameters']}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 50)
print("SPECIFIC DELETE TEST COMPLETE!")
print("Expected: 'buy apples' task should be deleted")
print("=" * 50)