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

print("=== Testing Chatbot Response Patterns ===\n")

# Test various command patterns to see how the simulated agent handles them
test_cases = [
    {"message": "Add a task to buy milk", "description": "Add task command"},
    {"message": "List all my tasks", "description": "List all tasks command"},
    {"message": "Show me pending tasks", "description": "List pending tasks command"},
    {"message": "Add task: call mom", "description": "Alternative add task format"},
    {"message": "help me", "description": "Help/unrecognized command"}
]

for i, test_case in enumerate(test_cases, 1):
    print(f"{i}. {test_case['description']}: '{test_case['message']}'")
    chat_data = {
        "message": test_case['message'],
        "conversation_id": None  # Start new conversation for each test
    }

    try:
        response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result['response']}")
            print(f"   Tool Calls: {len(result['tool_calls'])} tool(s) called")
            if result['tool_calls']:
                for tool_call in result['tool_calls']:
                    print(f"     - {tool_call['name']}: {tool_call['parameters']}")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    print()