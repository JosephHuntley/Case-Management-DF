def test_create_chain_of_custody(client, db_session):
    user = client.post("/users/", json={
        "username": "custodyuser1",
        "email": "custodyuser1@example.com",
        "password": "password123",
        "role": "investigator"
    })
    case = client.post("/cases/", json={
        "title": "Test Case for Chain of Custody",
        "description": "This case is for testing creation of chain of custody records",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })

    
    response = client.post("/chain-of-custody/", json={
        "case_id": case.json()["id"],
        "item_description": "Test evidence item",
        "collected_by": user.json()["id"],
        "notes": "Initial collection of evidence",
        evidence_id: "11111111-1111-1111-1111-111111111111",
    })