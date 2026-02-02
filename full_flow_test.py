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

print("TODOBOOM AI CHATBOT - FULL FLOW TEST")
print("=" * 50)

# Step 1: List all tasks first to see what we have
print("\n1. Listing all tasks first:")
chat_data = {
    "message": "list all tasks",
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

# Step 2: Try to delete a specific existing task
print("\n2. Trying to delete an existing task 'buy milk':")
chat_data = {
    "message": "delete buy milk",
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

# Step 3: List tasks again to see if deletion happened
print("\n3. Listing tasks again to verify:")
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
print("FULL FLOW TEST COMPLETE!")
print("Expected: 'buy milk' task should be deleted if it existed")
print("=" * 50)