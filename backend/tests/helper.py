from uuid import uuid4

def create_test_user(client, username=None, role="investigator"):
    if username is None:
        username = f"testuser{uuid4()}"
    return client.post("/api/users/", json={
        "username": username,
        "email": f"{username}@example.com",
        "password": "password123",
        "role": role,
        "first_name": "John",
        "last_name": "Doe"
    })

def create_test_case(client, user=None, title=None):
    if user is None:
        user = create_test_user(client)
    if title is None:
        title = f"test case {uuid4()}"
    
    return client.post("/api/cases/", json={
        "title": title,
        "description": "This case is for testing case notes",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })

    