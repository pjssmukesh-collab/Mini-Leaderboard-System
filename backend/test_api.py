import requests

url = "http://127.0.0.1:8000/auth/register"
payload = {
    "name": "Test User",
    "email": "test12345@example.com",
    "password": "password123",
    "role": "player"
}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
