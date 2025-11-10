from backend.app.services.extract import (
    extract_action_items,
    extract_action_items_enhanced,
    extract_action_items_with_priority,
    extract_due_date,
)


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "ACTION: review PR" in items
    assert "Ship it!" in items


def test_extract_action_items_with_priority():
    text = """
TODO: regular task
TODO: URGENT fix the bug!!
Action: low priority task?
Fix: important security issue
Random text
Task: ASAP complete this
    """
    items = extract_action_items_with_priority(text)

    assert len(items) == 5

    regular = next(item for item in items if "regular task" in item["text"])
    assert regular["priority"] == "medium"

    urgent = next(item for item in items if "URGENT" in item["text"])
    assert urgent["priority"] == "high"

    low = next(item for item in items if "low priority" in item["text"])
    assert low["priority"] == "low"

    security = next(item for item in items if "security" in item["text"])
    assert security["priority"] == "high"

    asap = next(item for item in items if "ASAP" in item["text"])
    assert asap["priority"] == "high"


def test_extract_due_date():
    assert extract_due_date("TODO: Fix bug due: 2024-11-15") == "2024-11-15"
    assert extract_due_date("Action: Send email by 2024-12-01") == "2024-12-01"
    assert extract_due_date("Task: Complete deadline: 2024-11-20") == "2024-11-20"
    assert extract_due_date("TODO: No due date") is None
    assert extract_due_date("Fix: Bug due: 12/25/2024") == "2024-12-25"
    assert extract_due_date("Task: Invalid date due: 2024-13-45") is None


def test_extract_action_items_enhanced():
    text = """
TODO: Regular task
TODO: URGENT fix bug due: 2024-11-20!!
Action: Check email?
Fix: Critical issue ASAP by 2024-11-15
Random text here
Task: Implement feature deadline: 2024-12-01
    """
    items = extract_action_items_enhanced(text)

    assert len(items) == 5

    regular = next(item for item in items if "Regular task" in item["text"])
    assert regular["priority"] == "medium"
    assert regular["due_date"] is None

    urgent = next(item for item in items if "URGENT" in item["text"])
    assert urgent["priority"] == "high"
    assert urgent["due_date"] == "2024-11-20"

    low = next(item for item in items if "Check email" in item["text"])
    assert low["priority"] == "low"
    assert low["due_date"] is None

    critical = next(item for item in items if "Critical" in item["text"])
    assert critical["priority"] == "high"
    assert critical["due_date"] == "2024-11-15"

    feature = next(item for item in items if "feature" in item["text"])
    assert feature["priority"] == "medium"
    assert feature["due_date"] == "2024-12-01"


def test_extract_action_items_with_bullet_points():
    text = """
- TODO: Task with bullet
- Action: Another task
- Just regular text
- Fix: Bug with urgency!!
    """
    items = extract_action_items_enhanced(text)

    assert len(items) == 3
    assert any("Task with bullet" in item["text"] for item in items)
    assert any("Another task" in item["text"] for item in items)

    urgent = next(item for item in items if "urgency" in item["text"])
    assert urgent["priority"] == "high"


def test_extract_multiple_action_keywords():
    text = """
Bug: Fix the login issue
Task: Update documentation
Fix: Memory leak
TODO: Refactor code
    """
    items = extract_action_items_with_priority(text)

    assert len(items) == 4
    assert all(item["priority"] in ["low", "medium", "high"] for item in items)
