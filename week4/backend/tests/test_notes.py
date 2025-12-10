def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_update_note_success(client):
    """Test updating an existing note with valid data."""
    create_payload = {"title": "Original Title", "content": "Original content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    update_payload = {"title": "Updated Title", "content": "Updated content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == note_id
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"


def test_update_note_partial(client):
    """Test partially updating a note (only title or content)."""
    create_payload = {"title": "Original Title", "content": "Original content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    update_payload = {"title": "Updated Title"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Original content"


def test_update_note_not_found(client):
    """Test updating a non-existent note returns 404."""
    update_payload = {"title": "Updated", "content": "Updated"}
    r = client.put("/notes/9999", json=update_payload)
    assert r.status_code == 404


def test_delete_note_success(client):
    """Test deleting an existing note."""
    create_payload = {"title": "To Delete", "content": "Will be deleted"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_note_not_found(client):
    """Test deleting a non-existent note returns 404."""
    r = client.delete("/notes/9999")
    assert r.status_code == 404


def test_search_notes_no_results(client):
    """Test searching for notes with no matches."""
    r = client.get("/notes/search/", params={"q": "nonexistentquery12345"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 0


def test_get_note_success(client):
    """Test retrieving a specific note by ID."""
    create_payload = {"title": "Specific Note", "content": "Specific content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == note_id
    assert data["title"] == "Specific Note"
