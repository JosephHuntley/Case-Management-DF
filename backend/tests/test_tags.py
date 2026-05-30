from uuid import uuid4

def test_create_tag(client):
    response = client.post(
        "/tags/",
        json={
            "name": "Test Tag",
            "description": "This is a test tag",
            "color": "#FF5733"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Test Tag"
    assert data["description"] == "This is a test tag"
    assert data["color"] == "#FF5733"
    assert "id" in data

def test_get_tags(client):
    response = client.get("/tags/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_tag(client):
    created = client.post(
        "/tags/",
        json={
            "name": "Update Tag",
            "description": "This tag will be updated",
            "color": "#33FF57"
        }
    )

    assert created.status_code == 200
    tag_id = created.json()["id"]

    response = client.put(
        f"/tags/{tag_id}",
        json={
            "name": "Updated Tag",
            "description": "This tag has been updated",
            "color": "#3357FF"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Tag"
    assert data["description"] == "This tag has been updated"
    assert data["color"] == "#3357FF"

def test_delete_tag(client):
    created = client.post(
        "/tags/",
        json={
            "name": "Delete Tag",
            "description": "This tag will be deleted",
            "color": "#FF33A1"
        }
    )

    assert created.status_code == 200
    tag_id = created.json()["id"]

    response = client.delete(f"/tags/{tag_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Tag deleted successfully"

    response = client.get("/tags/")
    deleted_tag = [t for t in response.json() if t["id"] == tag_id]
    assert len(deleted_tag) == 0