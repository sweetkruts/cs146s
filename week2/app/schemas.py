"""
Pydantic schemas for API request/response validation.

This module defines well-typed data models for all API endpoints,
replacing loose Dict[str, Any] types with structured validation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Note Schemas
# ============================================================================


class NoteCreate(BaseModel):
    """Request schema for creating a new note."""

    content: str = Field(..., min_length=1, description="Note content text")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"content": "Meeting notes:\n- Implement new feature\n- Fix bug"}
        }
    )


class NoteResponse(BaseModel):
    """Response schema for note data."""

    id: int = Field(..., description="Note ID")
    content: str = Field(..., description="Note content")
    created_at: str = Field(..., description="Creation timestamp")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "content": "Meeting notes",
                "created_at": "2024-01-01 12:00:00",
            }
        }
    )


# ============================================================================
# Action Item Schemas
# ============================================================================


class ActionItemExtractRequest(BaseModel):
    """Request schema for extracting action items from text."""

    text: str = Field(..., min_length=1, description="Text to extract action items from")
    save_note: bool = Field(
        default=False, description="Whether to save the input text as a note"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "TODO: Implement feature\n- Write tests\n- Update docs",
                "save_note": True,
            }
        }
    )


class ActionItemResponse(BaseModel):
    """Response schema for a single action item."""

    id: int = Field(..., description="Action item ID")
    text: str = Field(..., description="Action item text")
    note_id: Optional[int] = Field(default=None, description="Associated note ID")
    done: bool = Field(default=False, description="Whether the item is completed")
    created_at: str = Field(..., description="Creation timestamp")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "text": "Implement feature",
                "note_id": 1,
                "done": False,
                "created_at": "2024-01-01 12:00:00",
            }
        }
    )


class ActionItemExtractResponse(BaseModel):
    """Response schema for extraction results."""

    note_id: Optional[int] = Field(default=None, description="Created note ID if saved")
    items: list[dict] = Field(..., description="Extracted action items")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "note_id": 1,
                "items": [
                    {"id": 1, "text": "Implement feature"},
                    {"id": 2, "text": "Write tests"},
                ],
            }
        }
    )


class ActionItemUpdateRequest(BaseModel):
    """Request schema for updating an action item's completion status."""

    done: bool = Field(..., description="Completion status")

    model_config = ConfigDict(json_schema_extra={"example": {"done": True}})


class ActionItemUpdateResponse(BaseModel):
    """Response schema for action item update."""

    id: int = Field(..., description="Action item ID")
    done: bool = Field(..., description="Updated completion status")

    model_config = ConfigDict(json_schema_extra={"example": {"id": 1, "done": True}})


# ============================================================================
# Error Schemas
# ============================================================================


class ErrorResponse(BaseModel):
    """Standard error response schema."""

    detail: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(default=None, description="Error type/category")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"detail": "Resource not found", "error_type": "NotFoundError"}
        }
    )

