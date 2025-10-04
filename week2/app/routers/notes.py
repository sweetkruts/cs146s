"""
Notes router with well-defined API contracts.

Handles creation and retrieval of notes using Pydantic schemas
for request/response validation.
"""

from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..schemas import NoteCreate, NoteResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={
        404: {"model": ErrorResponse, "description": "Note not found"},
        500: {"model": ErrorResponse, "description": "Database error"},
    },
)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Create a new note with the provided content",
)
def create_note(payload: NoteCreate) -> NoteResponse:
    """
    Create a new note.
    
    Args:
        payload: Note creation request with content
        
    Returns:
        The created note with ID and timestamp
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        note_id = db.insert_note(payload.content)
        note = db.get_note(note_id)
        
        if note is None:
            # Should never happen, but handle defensively
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created note",
            )
        
        return NoteResponse(
            id=note["id"],
            content=note["content"],
            created_at=note["created_at"],
        )
    except ValueError as e:
        logger.warning(f"Invalid note data: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create note: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note",
        )


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
    summary="Get a note by ID",
    description="Retrieve a single note by its ID",
)
def get_single_note(note_id: int) -> NoteResponse:
    """
    Get a single note by ID.
    
    Args:
        note_id: The note ID to retrieve
        
    Returns:
        The note data
        
    Raises:
        HTTPException: If note not found or retrieval fails
    """
    try:
        row = db.get_note(note_id)
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note {note_id} not found",
            )
        
        return NoteResponse(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get note {note_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve note",
        )


@router.get(
    "",
    response_model=List[NoteResponse],
    summary="List all notes",
    description="Retrieve all notes in descending order by ID",
)
def list_all_notes() -> List[NoteResponse]:
    """
    List all notes.
    
    Returns:
        List of all notes
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        rows = db.list_notes()
        return [
            NoteResponse(
                id=row["id"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Failed to list notes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notes",
        )


