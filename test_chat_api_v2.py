import requests
import json
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

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

print("Testing basic API...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Error connecting to API: {e}")

# Test health endpoint
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health endpoint: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Error connecting to health endpoint: {e}")

# Test chat endpoint with a manually created token for user ID 1
print("\nTesting chat endpoint with manual token...")

# Create a test token for user ID 1
test_token = create_test_token(1)
headers = {
    "Authorization": f"Bearer {test_token}",
    "Content-Type": "application/json"
}

# Test chat endpoint
chat_data = {
    "message": "Hello, can you help me add a task?",
    "conversation_id": None
}

try:
    response = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data, headers=headers)
    print(f"Chat endpoint response: {response.status_code}")
    if response.status_code == 200:
        chat_result = response.json()
        print(f"Chat response: {json.dumps(chat_result, indent=2)}")
    else:
        print(f"Chat error: {response.text}")
        print(f"Headers sent: {headers}")
        print(f"Data sent: {chat_data}")

        # Let's also test the endpoint without auth to see the error
        try:
            response_no_auth = requests.post(f"{BASE_URL}/api/1/chat", json=chat_data)
            print(f"Response without auth: {response_no_auth.status_code} - {response_no_auth.text}")
        except Exception as e:
            print(f"Error testing without auth: {e}")

except Exception as e:
    print(f"Error calling chat endpoint: {e}")
    print(f"Token created: {test_token}")

# Test the test endpoint
try:
    response = requests.get(f"{BASE_URL}/api/1/chat/test", headers=headers)
    print(f"Chat test endpoint: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Error calling chat test endpoint: {e}")