from uuid import uuid4

def test_create_case(client):
    user = client.post(
        "/users/",
        json={
            "username": "caseuser",
            "email": "caseuser@test.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert user.status_code == 200
    user_id = user.json()["id"]

    response = client.post(
        "/cases/",
        json={
            "title": "Test Case",
            "description": "This is a test case",
            "status": "open",
            "priority": "medium",
            "created_by": user_id
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Case"
    assert data["description"] == "This is a test case"
    assert data["status"] == "open"
    assert data["priority"] == "medium"
    assert "id" in data
    
def test_get_cases(client):
    response = client.get("/cases/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_case(client):
    user = client.post(
        "/users/",
        json={
            "username": "caseuser2",
            "email": "caseuser2@test.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert user.status_code == 200
    user_id = user.json()["id"]

    created = client.post(
        "/cases/",
        json={
            "title": "Test Case",
            "description": "This is a test case",
            "status": "open",
            "priority": "medium",
            "created_by": user_id
        }
    )

    assert created.status_code == 200
    case_id = created.json()["id"]

    response = client.get(f"/cases/{case_id}")
    assert response.status_code == 200
    assert response.json()["id"] == case_id

def test_get_missing_cases(client):
    response = client.get(f"/cases/{uuid4()}")

    assert response.status_code == 404

def test_update_case(client):
    user = client.post(
        "/users/",
        json={
            "username": "caseuser3",
            "email": "caseuser3@test.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert user.status_code == 200
    user_id = user.json()["id"]

    created = client.post(
        "/cases/",
        json={
            "title": "Test Case",
            "description": "This is a test case",
            "status": "open",
            "priority": "medium",
            "created_by": user_id
        }
    )

    assert created.status_code == 200
    case_id = created.json()["id"]

    response = client.put(
        f"/cases/{case_id}",
        json={
            "title": "Updated Test Case",
            "description": "This is an updated test case",
            "status": "in progress",
            "priority": "high"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == case_id
    assert response.json()["title"] == "Updated Test Case"
    assert response.json()["description"] == "This is an updated test case"
    assert response.json()["status"] == "in progress"
    assert response.json()["priority"] == "high"

def test_delete_case(client):
    user = client.post(
        "/users/",
        json={
            "username": "caseuser4",
            "email": "caseuser4@test.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert user.status_code == 200
    user_id = user.json()["id"]

    created = client.post(
        "/cases/",
        json={
            "title": "Test Case",
            "description": "This is a test case",
            "status": "open",
            "priority": "medium",
            "created_by": user_id
        }
    )

    assert created.status_code == 200
    case_id = created.json()["id"]

    response = client.delete(f"/cases/{case_id}")
    assert response.status_code == 200

    get_all = client.get("/cases/")
    case_ids = [c["id"] for c in get_all.json()]
    assert case_id not in case_ids

    # Since it's a soft delete, we should still be able to get the case by ID, but it should be marked as deleted. 
    response = client.get(f"/cases/{case_id}")
    assert response.status_code == 200
    assert response.json()["deleted_at"] is not None

