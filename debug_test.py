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

print("TODOBOOM AI CHATBOT - DEBUGGING TEST")
print("=" * 40)

# Test with a simple list command that should work
print("\n1. Testing simple 'list tasks' command:")
chat_data = {
    "message": "list tasks",
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
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test with a simple delete command after seeing what tasks exist
print("\n2. Testing 'delete task' command:")
chat_data = {
    "message": "delete task",
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