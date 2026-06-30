from uuid import uuid4

def create_test_user(client, username=f"testuser{uuid4()}", role="investigator"):
    return client.post("/users/", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": "password123",
        "role": role,
    })