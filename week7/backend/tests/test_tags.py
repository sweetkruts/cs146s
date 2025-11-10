def test_create_and_list_tags(client):
    r = client.post("/tags/", json={"name": "work", "color": "#FF5733"})
    assert r.status_code == 201
    tag = r.json()
    assert tag["name"] == "work"
    assert tag["color"] == "#FF5733"
    assert "created_at" in tag

    r = client.get("/tags/")
    assert r.status_code == 200
    tags = r.json()
    assert len(tags) >= 1


def test_get_tag_by_id(client):
    r = client.post("/tags/", json={"name": "personal"})
    tag_id = r.json()["id"]

    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "personal"


def test_patch_tag(client):
    r = client.post("/tags/", json={"name": "oldname"})
    tag_id = r.json()["id"]

    r = client.patch(f"/tags/{tag_id}", json={"name": "newname", "color": "#00FF00"})
    assert r.status_code == 200
    updated = r.json()
    assert updated["name"] == "newname"
    assert updated["color"] == "#00FF00"


def test_delete_tag(client):
    r = client.post("/tags/", json={"name": "to_delete"})
    tag_id = r.json()["id"]

    r = client.delete(f"/tags/{tag_id}")
    assert r.status_code == 204

    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 404


def test_duplicate_tag_name(client):
    client.post("/tags/", json={"name": "duplicate"})
    r = client.post("/tags/", json={"name": "duplicate"})
    assert r.status_code == 400
    assert "already exists" in r.json()["detail"]


def test_tag_color_validation(client):
    r = client.post("/tags/", json={"name": "test", "color": "invalid"})
    assert r.status_code == 422

    r = client.post("/tags/", json={"name": "test", "color": "#GGGGGG"})
    assert r.status_code == 422

    r = client.post("/tags/", json={"name": "test", "color": "#123"})
    assert r.status_code == 422


def test_create_note_with_tags(client):
    r1 = client.post("/tags/", json={"name": "urgent"})
    r2 = client.post("/tags/", json={"name": "review"})
    tag1_id = r1.json()["id"]
    tag2_id = r2.json()["id"]

    r = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "Content", "tag_ids": [tag1_id, tag2_id]},
    )
    assert r.status_code == 201
    note = r.json()
    assert len(note["tags"]) == 2
    tag_names = [tag["name"] for tag in note["tags"]]
    assert "urgent" in tag_names
    assert "review" in tag_names


def test_create_note_with_invalid_tag(client):
    r = client.post(
        "/notes/",
        json={"title": "Test", "content": "Content", "tag_ids": [99999]},
    )
    assert r.status_code == 400
    assert "not found" in r.json()["detail"]


def test_patch_note_tags(client):
    r1 = client.post("/tags/", json={"name": "tag1"})
    r2 = client.post("/tags/", json={"name": "tag2"})
    r3 = client.post("/tags/", json={"name": "tag3"})
    tag1_id = r1.json()["id"]
    tag2_id = r2.json()["id"]
    tag3_id = r3.json()["id"]

    r = client.post(
        "/notes/",
        json={"title": "Note", "content": "Content", "tag_ids": [tag1_id, tag2_id]},
    )
    note_id = r.json()["id"]

    r = client.patch(f"/notes/{note_id}", json={"tag_ids": [tag3_id]})
    assert r.status_code == 200
    updated = r.json()
    assert len(updated["tags"]) == 1
    assert updated["tags"][0]["name"] == "tag3"


def test_delete_tag_removes_from_notes(client):
    r = client.post("/tags/", json={"name": "temp_tag"})
    tag_id = r.json()["id"]

    r = client.post(
        "/notes/",
        json={"title": "Note", "content": "Content", "tag_ids": [tag_id]},
    )
    note_id = r.json()["id"]

    r = client.delete(f"/tags/{tag_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert len(r.json()["tags"]) == 0


def test_tag_sorting(client):
    client.post("/tags/", json={"name": "zebra"})
    client.post("/tags/", json={"name": "apple"})

    r = client.get("/tags/", params={"sort": "name"})
    assert r.status_code == 200
    tags = r.json()
    assert tags[0]["name"] == "apple"
    assert tags[1]["name"] == "zebra"
