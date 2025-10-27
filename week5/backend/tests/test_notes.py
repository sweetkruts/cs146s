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
    """Test updating an existing note."""
    create_payload = {"title": "Original", "content": "Original content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    update_payload = {"title": "Updated", "content": "Updated content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Updated"
    assert data["content"] == "Updated content"


def test_update_note_partial(client):
    """Test partial update (only content)."""
    create_payload = {"title": "Original", "content": "Original content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    update_payload = {"content": "Updated content only"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Original"
    assert data["content"] == "Updated content only"


def test_update_note_not_found(client):
    """Test updating non-existent note returns 404."""
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
    """Test deleting non-existent note returns 404."""
    r = client.delete("/notes/9999")
    assert r.status_code == 404


def test_create_note_validation_error(client):
    """Test creating note with invalid data returns 422 with error envelope."""
    payload = {"title": "", "content": "Valid content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    data = r.json()
    assert data["ok"] is False
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_error_response_envelope(client):
    """Test that 404 errors return proper envelope structure."""
    r = client.get("/notes/9999")
    assert r.status_code == 404
    data = r.json()
    assert data["ok"] is False
    assert "error" in data
    assert data["error"]["code"] == 404
    assert "not found" in data["error"]["message"].lower()


def test_create_note_with_max_length_content(client):
    """Test creating note with maximum length content."""
    max_content = "x" * 5000
    payload = {"title": "Max Content Test", "content": max_content}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["content"] == max_content


def test_create_note_content_too_long(client):
    """Test creating note with content exceeding max length."""
    too_long_content = "x" * 5001
    payload = {"title": "Too Long", "content": too_long_content}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
    data = r.json()
    assert data["ok"] is False


def test_search_notes_with_special_characters(client):
    """Test searching notes with special characters."""
    payload = {"title": "Special!", "content": "Test with @#$%"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201

    r = client.get("/notes/search/", params={"q": "@#$"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_search_notes_no_results(client):
    """Test searching notes with query that has no matches."""
    r = client.get("/notes/search/", params={"q": "nonexistentquery12345xyz"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 0


def test_update_note_with_empty_update(client):
    """Test updating note without providing any fields."""
    create_payload = {"title": "Original", "content": "Original content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    update_payload = {}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Original"
    assert data["content"] == "Original content"
