def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_delete_note(client):
    r = client.post("/notes/", json={"title": "To Delete", "content": "Will be deleted"})
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_nonexistent_note(client):
    r = client.delete("/notes/99999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_note_validation_empty_title(client):
    r = client.post("/notes/", json={"title": "", "content": "Valid content"})
    assert r.status_code == 422


def test_note_validation_empty_content(client):
    r = client.post("/notes/", json={"title": "Valid title", "content": ""})
    assert r.status_code == 422


def test_note_validation_title_too_long(client):
    long_title = "x" * 201
    r = client.post("/notes/", json={"title": long_title, "content": "Valid"})
    assert r.status_code == 422


def test_note_patch_validation(client):
    r = client.post("/notes/", json={"title": "Original", "content": "Content"})
    note_id = r.json()["id"]

    r = client.patch(f"/notes/{note_id}", json={"title": ""})
    assert r.status_code == 422


def test_get_note_by_id(client):
    r = client.post("/notes/", json={"title": "Specific", "content": "Note"})
    note_id = r.json()["id"]

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Specific"
