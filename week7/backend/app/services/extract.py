import re
from datetime import datetime


def extract_action_items(text: str) -> list[str]:
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[str] = []
    for line in lines:
        normalized = line.lower()
        if normalized.startswith("todo:") or normalized.startswith("action:"):
            results.append(line)
        elif line.endswith("!"):
            results.append(line)
    return results


def extract_action_items_with_priority(text: str) -> list[dict[str, str]]:
    """
    Extract action items with priority levels based on keywords and urgency markers.
    Returns list of dicts with 'text' and 'priority' keys.
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[dict[str, str]] = []

    high_priority_keywords = ["urgent", "asap", "critical", "important", "emergency"]
    action_keywords = ["todo:", "action:", "task:", "fix:", "bug:"]

    for line in lines:
        normalized = line.lower()

        if any(normalized.startswith(kw) for kw in action_keywords) or line.endswith("!"):
            priority = "medium"

            if any(kw in normalized for kw in high_priority_keywords) or line.endswith("!!"):
                priority = "high"
            elif line.endswith("?"):
                priority = "low"

            results.append({"text": line, "priority": priority})

    return results


def extract_due_date(text: str) -> str | None:
    """
    Extract due date from text. Returns ISO format date string if found.
    Patterns: 'due: YYYY-MM-DD', 'by YYYY-MM-DD', 'deadline: MM/DD/YYYY'
    """
    date_patterns = [
        r"due:\s*(\d{4}-\d{2}-\d{2})",
        r"by\s+(\d{4}-\d{2}-\d{2})",
        r"deadline:\s*(\d{4}-\d{2}-\d{2})",
        r"due:\s*(\d{1,2}/\d{1,2}/\d{4})",
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text.lower())
        if match:
            date_str = match.group(1)
            try:
                if "/" in date_str:
                    parsed = datetime.strptime(date_str, "%m/%d/%Y")
                else:
                    parsed = datetime.strptime(date_str, "%Y-%m-%d")
                return parsed.strftime("%Y-%m-%d")
            except ValueError:
                continue

    return None


def extract_action_items_enhanced(text: str) -> list[dict[str, str | None]]:
    """
    Enhanced extraction with priority, due date, and categorization.
    Returns list of dicts with 'text', 'priority', and 'due_date' keys.
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[dict[str, str | None]] = []

    high_priority_keywords = ["urgent", "asap", "critical", "important", "emergency"]
    action_keywords = ["todo:", "action:", "task:", "fix:", "bug:"]

    for line in lines:
        normalized = line.lower()

        if any(normalized.startswith(kw) for kw in action_keywords) or line.endswith(("!", "!!")):
            priority = "medium"

            if any(kw in normalized for kw in high_priority_keywords) or line.endswith("!!"):
                priority = "high"
            elif line.endswith("?"):
                priority = "low"

            due_date = extract_due_date(line)

            results.append({"text": line, "priority": priority, "due_date": due_date})

    return results
