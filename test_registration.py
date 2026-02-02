import requests
import json

BASE_URL = "http://localhost:8000"

print("Testing Registration Functionality")
print("=" * 40)

# Test registration with a new user
registration_data = {
    "email": "test_user_" + str(hash("test"))[-6:] + "@example.com",  # Create unique email
    "password": "testpassword123",
    "name": "Test User"
}

print(f"Attempting to register user: {registration_data['email']}")

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=registration_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        print("✅ Registration successful!")
        result = response.json()
        if 'data' in result and 'token' in result['data']:
            print("✅ Token received")
        else:
            print("? Token not found in response")
    elif response.status_code == 409:
        print("❌ Registration failed - email already exists")
    else:
        print(f"❌ Registration failed with status {response.status_code}")

except Exception as e:
    print(f"❌ Error during registration: {e}")

print("\nTesting Login with existing user...")
# Try to login with a default user
login_data = {
    "email": "admin@example.com",
    "password": "password123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login Status Code: {response.status_code}")
    print(f"Login Response: {response.text}")
except Exception as e:
    print(f"❌ Error during login: {e}")

print("\nTesting existing users in database...")
# Let's check what users exist in the database
try:
    from sqlmodel import create_engine, Session, select
    from backend.src.models.user_task_models import User
    from backend.src.database.session import DATABASE_URL

    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print(f"Found {len(users)} users in database:")
        for user in users[:5]:  # Show first 5 users
            print(f"  - ID: {user.id}, Email: {user.email}, Name: {user.name}")
        if len(users) > 5:
            print(f"  ... and {len(users) - 5} more users")
except Exception as e:
    print(f"❌ Error checking database users: {e}")