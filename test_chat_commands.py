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

print("=== Testing Different Chat Commands ===\n")

# Test 1: Add a task
print("1. Testing add task command...")
chat_data = {
    "message": "Add a task to buy groceries for tomorrow",
    "conversation_id": None
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['response']}")
        print(f"Tool calls: {result['tool_calls']}")
        conversation_id = result['conversation_id']
        print(f"Conversation ID: {conversation_id}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 2: List tasks (using the conversation ID from previous response)
print("2. Testing list tasks command...")
chat_data = {
    "message": "Show me my tasks",
    "conversation_id": conversation_id  # Use the conversation ID to continue the conversation
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response']}")
        print(f"Tool calls: {result['tool_calls']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 3: Complete a task (this would require knowing a task ID)
print("3. Testing complete task command...")
chat_data = {
    "message": "Mark the grocery task as complete",
    "conversation_id": conversation_id
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response']}")
        print(f"Tool calls: {result['tool_calls']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 4: Update a task
print("4. Testing update task command...")
chat_data = {
    "message": "Update the grocery task to say 'buy groceries for tonight'",
    "conversation_id": conversation_id
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response']}")
        print(f"Tool calls: {result['tool_calls']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50 + "\n")

# Test 5: Delete a task
print("5. Testing delete task command...")
chat_data = {
    "message": "Delete the grocery task",
    "conversation_id": conversation_id
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"Response: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result['response']}")
        print(f"Tool calls: {result['tool_calls']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")