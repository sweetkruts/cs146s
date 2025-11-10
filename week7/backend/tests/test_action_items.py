def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_delete_action_item(client):
    r = client.post("/action-items/", json={"description": "To be deleted"})
    assert r.status_code == 201
    item_id = r.json()["id"]

    r = client.delete(f"/action-items/{item_id}")
    assert r.status_code == 204

    r = client.get(f"/action-items/{item_id}")
    assert r.status_code == 404


def test_delete_nonexistent_action_item(client):
    r = client.delete("/action-items/99999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_action_item_validation_empty_description(client):
    r = client.post("/action-items/", json={"description": ""})
    assert r.status_code == 422


def test_action_item_validation_too_long(client):
    long_desc = "x" * 501
    r = client.post("/action-items/", json={"description": long_desc})
    assert r.status_code == 422


def test_action_item_patch_validation(client):
    r = client.post("/action-items/", json={"description": "Original"})
    item_id = r.json()["id"]

    r = client.patch(f"/action-items/{item_id}", json={"description": ""})
    assert r.status_code == 422


def test_get_action_item_by_id(client):
    r = client.post("/action-items/", json={"description": "Specific item"})
    item_id = r.json()["id"]

    r = client.get(f"/action-items/{item_id}")
    assert r.status_code == 200
    assert r.json()["description"] == "Specific item"
