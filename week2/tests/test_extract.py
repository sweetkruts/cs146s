import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ============================================================================
# Tests for extract_action_items_llm()
# ============================================================================

def test_llm_extract_bullet_list():
    """Test LLM extraction with standard bullet points."""
    text = """
    Meeting notes:
    - Set up database
    - Implement API endpoint
    - Write documentation
    Some random narrative text here.
    """.strip()
    
    items = extract_action_items_llm(text)
    
    # LLM should extract the three action items
    assert len(items) >= 3
    assert any("database" in item.lower() for item in items)
    assert any("api" in item.lower() or "endpoint" in item.lower() for item in items)
    assert any("documentation" in item.lower() for item in items)


def test_llm_extract_keyword_prefixed():
    """Test LLM extraction with keyword prefixes."""
    text = """
    TODO: Update user authentication
    Action: Refactor database queries
    Next: Deploy to production
    """.strip()
    
    items = extract_action_items_llm(text)
    
    # Should extract all three keyword-prefixed items
    assert len(items) >= 3
    assert any("authentication" in item.lower() for item in items)
    assert any("refactor" in item.lower() or "database" in item.lower() for item in items)
    assert any("deploy" in item.lower() or "production" in item.lower() for item in items)


def test_llm_extract_empty_input():
    """Test LLM extraction with empty input."""
    # Test empty string
    items = extract_action_items_llm("")
    assert items == []
    
    # Test whitespace only
    items = extract_action_items_llm("   \n  \t  ")
    assert items == []


def test_llm_extract_no_action_items():
    """Test LLM extraction with text containing no action items."""
    text = """
    This is a regular paragraph describing the weather.
    It's sunny today and the temperature is pleasant.
    There are no tasks or action items here.
    """.strip()
    
    items = extract_action_items_llm(text)
    
    # Should return empty or very few items (LLM might interpret some text as actions)
    assert len(items) <= 1


def test_llm_extract_mixed_format():
    """Test LLM extraction with mixed formatting styles."""
    text = """
    Project Tasks:
    1. Create database schema
    - [ ] Write unit tests
    TODO: Update README
    * Fix bug in login page
    Next: Schedule team meeting
    """.strip()
    
    items = extract_action_items_llm(text)
    
    # Should extract all action items regardless of format
    assert len(items) >= 5
    assert any("database" in item.lower() or "schema" in item.lower() for item in items)
    assert any("test" in item.lower() for item in items)
    assert any("readme" in item.lower() for item in items)
    assert any("bug" in item.lower() or "login" in item.lower() for item in items)
    assert any("meeting" in item.lower() for item in items)


def test_llm_extract_numbered_list():
    """Test LLM extraction with numbered lists."""
    text = """
    Development roadmap:
    1. Design the API architecture
    2. Implement authentication layer
    3. Create frontend components
    4. Write integration tests
    """.strip()
    
    items = extract_action_items_llm(text)
    
    # Should extract all numbered items
    assert len(items) >= 4
    assert any("design" in item.lower() or "api" in item.lower() for item in items)
    assert any("authentication" in item.lower() for item in items)
    assert any("frontend" in item.lower() or "component" in item.lower() for item in items)
    assert any("test" in item.lower() for item in items)


def test_llm_extract_imperative_sentences():
    """Test LLM extraction with imperative sentences."""
    text = """
    Please complete the following:
    Fix the authentication bug.
    Update the API documentation.
    Review the pull request.
    """.strip()
    
    items = extract_action_items_llm(text)
    
    # Should extract imperative sentences as action items
    assert len(items) >= 3
    assert any("fix" in item.lower() or "authentication" in item.lower() for item in items)
    assert any("update" in item.lower() or "documentation" in item.lower() for item in items)
    assert any("review" in item.lower() or "pull request" in item.lower() for item in items)


def test_llm_extract_deduplication():
    """Test that LLM extraction deduplicates similar items."""
    text = """
    - Fix the login bug
    - Fix the login bug
    - fix the login bug
    """.strip()
    
    items = extract_action_items_llm(text)
    
    # Should return only one item (deduplicated)
    assert len(items) == 1


def test_llm_extract_checkbox_markers():
    """Test LLM extraction with checkbox markers."""
    text = """
    Sprint tasks:
    - [ ] Implement user registration
    - [x] Set up CI/CD pipeline
    - [todo] Write API documentation
    """.strip()
    
    items = extract_action_items_llm(text)
    
    # Should extract all items, including completed ones
    assert len(items) >= 2
    assert any("registration" in item.lower() for item in items)
    assert any("documentation" in item.lower() for item in items)
