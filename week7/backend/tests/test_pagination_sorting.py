def test_notes_pagination_basic(client):
    for i in range(10):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

    r = client.get("/notes/", params={"skip": 0, "limit": 5})
    assert r.status_code == 200
    assert len(r.json()) == 5

    r = client.get("/notes/", params={"skip": 5, "limit": 5})
    assert r.status_code == 200
    assert len(r.json()) == 5


def test_notes_pagination_skip_beyond_results(client):
    client.post("/notes/", json={"title": "Note 1", "content": "Content 1"})

    r = client.get("/notes/", params={"skip": 100, "limit": 10})
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_notes_pagination_limit_zero(client):
    client.post("/notes/", json={"title": "Note 1", "content": "Content 1"})

    r = client.get("/notes/", params={"limit": 0})
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_notes_pagination_max_limit(client):
    for i in range(250):
        client.post("/notes/", json={"title": f"Note {i}", "content": "Content"})

    r = client.get("/notes/", params={"limit": 200})
    assert r.status_code == 200
    assert len(r.json()) == 200

    r = client.get("/notes/", params={"limit": 250})
    assert r.status_code == 422


def test_notes_sorting_by_title_asc(client):
    client.post("/notes/", json={"title": "Zebra", "content": "Content"})
    client.post("/notes/", json={"title": "Apple", "content": "Content"})
    client.post("/notes/", json={"title": "Mango", "content": "Content"})

    r = client.get("/notes/", params={"sort": "title"})
    assert r.status_code == 200
    notes = r.json()
    titles = [n["title"] for n in notes]
    assert titles == sorted(titles)
    assert titles[0] == "Apple"


def test_notes_sorting_by_title_desc(client):
    client.post("/notes/", json={"title": "Zebra", "content": "Content"})
    client.post("/notes/", json={"title": "Apple", "content": "Content"})
    client.post("/notes/", json={"title": "Mango", "content": "Content"})

    r = client.get("/notes/", params={"sort": "-title"})
    assert r.status_code == 200
    notes = r.json()
    titles = [n["title"] for n in notes]
    assert titles == sorted(titles, reverse=True)
    assert titles[0] == "Zebra"


def test_notes_sorting_by_created_at(client):
    for i in range(3):
        client.post("/notes/", json={"title": f"Note {i}", "content": "Content"})

    r = client.get("/notes/", params={"sort": "created_at"})
    assert r.status_code == 200
    notes = r.json()
    created_times = [n["created_at"] for n in notes]
    assert created_times == sorted(created_times)

    r = client.get("/notes/", params={"sort": "-created_at"})
    assert r.status_code == 200
    notes = r.json()
    created_times = [n["created_at"] for n in notes]
    assert created_times == sorted(created_times, reverse=True)


def test_notes_sorting_invalid_field(client):
    client.post("/notes/", json={"title": "Note", "content": "Content"})

    r = client.get("/notes/", params={"sort": "invalid_field"})
    assert r.status_code == 200


def test_notes_pagination_and_sorting_combined(client):
    for i in range(20):
        client.post("/notes/", json={"title": f"Note {i:02d}", "content": "Content"})

    r = client.get("/notes/", params={"skip": 5, "limit": 5, "sort": "title"})
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) == 5
    titles = [n["title"] for n in notes]
    assert titles == sorted(titles)


def test_action_items_pagination_basic(client):
    for i in range(10):
        client.post("/action-items/", json={"description": f"Item {i}"})

    r = client.get("/action-items/", params={"skip": 0, "limit": 5})
    assert r.status_code == 200
    assert len(r.json()) == 5

    r = client.get("/action-items/", params={"skip": 5, "limit": 5})
    assert r.status_code == 200
    assert len(r.json()) == 5


def test_action_items_sorting_by_description(client):
    client.post("/action-items/", json={"description": "Zebra task"})
    client.post("/action-items/", json={"description": "Apple task"})
    client.post("/action-items/", json={"description": "Mango task"})

    r = client.get("/action-items/", params={"sort": "description"})
    assert r.status_code == 200
    items = r.json()
    descriptions = [item["description"] for item in items]
    assert descriptions == sorted(descriptions)


def test_action_items_filter_with_pagination(client):
    for i in range(10):
        r = client.post("/action-items/", json={"description": f"Item {i}"})
        if i % 2 == 0:
            item_id = r.json()["id"]
            client.put(f"/action-items/{item_id}/complete")

    r = client.get("/action-items/", params={"completed": True, "limit": 3})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 3
    assert all(item["completed"] for item in items)


def test_action_items_sorting_by_completed_status(client):
    for i in range(5):
        r = client.post("/action-items/", json={"description": f"Item {i}"})
        if i < 2:
            item_id = r.json()["id"]
            client.put(f"/action-items/{item_id}/complete")

    r = client.get("/action-items/", params={"sort": "completed"})
    assert r.status_code == 200
    items = r.json()
    completed_statuses = [item["completed"] for item in items]
    assert completed_statuses == sorted(completed_statuses)


def test_pagination_with_search_query(client):
    client.post("/notes/", json={"title": "Python tutorial", "content": "Learn Python"})
    client.post("/notes/", json={"title": "Java guide", "content": "Learn Java"})
    client.post("/notes/", json={"title": "Python advanced", "content": "Advanced topics"})
    client.post("/notes/", json={"title": "JavaScript basics", "content": "JS intro"})

    r = client.get("/notes/", params={"q": "Python", "limit": 1})
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) == 1
    assert "Python" in notes[0]["title"]


def test_empty_results_pagination(client):
    r = client.get("/notes/", params={"skip": 0, "limit": 10})
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_pagination_boundary_conditions(client):
    client.post("/notes/", json={"title": "Note 1", "content": "Content 1"})
    client.post("/notes/", json={"title": "Note 2", "content": "Content 2"})

    r = client.get("/notes/", params={"skip": 1, "limit": 1})
    assert r.status_code == 200
    assert len(r.json()) == 1

    r = client.get("/notes/", params={"skip": 2, "limit": 10})
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_large_skip_value(client):
    for i in range(5):
        client.post("/notes/", json={"title": f"Note {i}", "content": "Content"})

    r = client.get("/notes/", params={"skip": 1000000, "limit": 10})
    assert r.status_code == 200
    assert len(r.json()) == 0


def test_default_pagination_and_sorting(client):
    for i in range(3):
        client.post("/notes/", json={"title": f"Note {i}", "content": "Content"})

    r = client.get("/notes/")
    assert r.status_code == 200
    notes = r.json()
    assert len(notes) <= 50
    created_times = [n["created_at"] for n in notes]
    assert created_times == sorted(created_times, reverse=True)

