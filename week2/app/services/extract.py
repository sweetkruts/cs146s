from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def extract_action_items_llm(text: str, model: str = "llama3.1:8b") -> List[str]:
    """
    Extract action items from text using an LLM via Ollama.
    
    This function uses structured outputs to ensure the LLM returns
    a JSON array of action items.
    
    Args:
        text: The input text to extract action items from
        model: The Ollama model to use (default: llama3.1:8b)
    
    Returns:
        List of extracted action items as strings
    
    Raises:
        Exception: If the LLM call fails or returns invalid data
    """
    # Handle empty input
    if not text or not text.strip():
        return []
    
    # Define the schema for structured output
    schema = {
        "type": "object",
        "properties": {
            "action_items": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of action items extracted from the text"
            }
        },
        "required": ["action_items"]
    }
    
    # Craft the prompt for action item extraction
    prompt = f"""Extract all action items from the following text. An action item is a task that needs to be done, typically indicated by:
- Bullet points or numbered lists
- Keywords like "TODO", "action", "next"
- Imperative verbs (e.g., "implement", "create", "fix", "update")
- Checkbox markers like [ ] or [todo]

Return only the action items themselves, cleaned of any bullet points, checkboxes, or prefixes.
If there are no action items, return an empty list.

Text:
{text}"""
    
    try:
        # Call Ollama with structured output format
        response = chat(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            format=schema,  # Enforce structured output
            options={
                "temperature": 0.1,  # Low temperature for consistency
            }
        )
        
        # Parse the response
        content = response.message.content
        result = json.loads(content)
        
        # Extract and validate action items
        action_items = result.get("action_items", [])
        
        # Filter out empty strings and deduplicate
        seen: set[str] = set()
        unique: List[str] = []
        for item in action_items:
            if isinstance(item, str) and item.strip():
                cleaned = item.strip()
                lowered = cleaned.lower()
                if lowered not in seen:
                    seen.add(lowered)
                    unique.append(cleaned)
        
        return unique
        
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse LLM response as JSON: {e}")
    except Exception as e:
        raise Exception(f"LLM extraction failed: {e}")
