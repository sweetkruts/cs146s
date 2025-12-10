def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def test_complete_nonexistent_action_item(client):
    """Test completing non-existent action item returns 404 with error envelope."""
    r = client.put("/action-items/9999/complete")
    assert r.status_code == 404
    data = r.json()
    assert data["ok"] is False
    assert "error" in data


def test_action_item_validation_error(client):
    """Test creating action item with invalid data returns 422."""
    payload = {"description": ""}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422
    data = r.json()
    assert data["ok"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_list_action_items_empty(client):
    """Test listing action items when none exist."""
    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)


def test_create_action_item_with_max_length(client):
    """Test creating action item with maximum length description."""
    max_description = "x" * 500
    payload = {"description": max_description}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["description"] == max_description
    assert data["completed"] is False


def test_create_action_item_exceeding_max_length(client):
    """Test creating action item with description exceeding max length."""
    too_long = "x" * 501
    payload = {"description": too_long}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422
    data = r.json()
    assert data["ok"] is False


def test_complete_already_completed_item(client):
    """Test completing an already completed action item."""
    payload = {"description": "Test item"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    item_id = r.json()["id"]

    r = client.put(f"/action-items/{item_id}/complete")
    assert r.status_code == 200
    assert r.json()["completed"] is True

    r = client.put(f"/action-items/{item_id}/complete")
    assert r.status_code == 200
    assert r.json()["completed"] is True
