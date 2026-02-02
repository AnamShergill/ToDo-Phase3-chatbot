import requests
import json

# Test the chat API
BASE_URL = "http://localhost:8000"

# First, let's test the basic API
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

# Test chat endpoint - this requires authentication, so let's first try to register/login
print("\nTesting authentication...")
try:
    # Try to register a test user
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Registration: {response.status_code}")
    if response.status_code == 200:
        print(f"Registration response: {response.json()}")
    else:
        print(f"Registration response: {response.text}")

    # Try to login
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        auth_response = response.json()
        print(f"Login response: {auth_response}")
        access_token = auth_response.get('access_token')
    else:
        print(f"Login response: {response.text}")
        # If user already exists, try to login with a default user
        login_data = {
            "email": "admin@example.com",  # Default admin user
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            auth_response = response.json()
            print(f"Default login response: {auth_response}")
            access_token = auth_response.get('access_token')
        else:
            print("Could not authenticate - trying without auth for testing")
            access_token = None

    # Now test the chat endpoint if we have a token
    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        print(f"\nTesting chat endpoint with token...")
        # Get user ID from token (this is typically decoded from JWT, but for simplicity let's assume user ID 1)
        # First, let's try to get user info if possible
        try:
            response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                user_id = user_info.get('id', 1)  # Fallback to user ID 1
                print(f"User info: {user_info}")
            else:
                user_id = 1  # Default to user ID 1
                print(f"Using default user ID: {user_id}")
        except:
            user_id = 1
            print(f"Using default user ID: {user_id}")

        # Test chat endpoint
        chat_data = {
            "message": "Hello, can you help me add a task?",
            "conversation_id": None
        }

        try:
            response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
            print(f"Chat endpoint response: {response.status_code}")
            if response.status_code == 200:
                chat_result = response.json()
                print(f"Chat response: {json.dumps(chat_result, indent=2)}")
            else:
                print(f"Chat error: {response.text}")
        except Exception as e:
            print(f"Error calling chat endpoint: {e}")
    else:
        print("Skipping chat test - no authentication token")

except Exception as e:
    print(f"Error during authentication test: {e}")