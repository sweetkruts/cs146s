"""
Action Items router with well-defined API contracts.

Handles extraction, retrieval, and updates of action items using
Pydantic schemas for request/response validation.
"""

from __future__ import annotations

import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from .. import db
from ..db import ActionItemNotFoundError
from ..schemas import (
    ActionItemExtractRequest,
    ActionItemExtractResponse,
    ActionItemResponse,
    ActionItemUpdateRequest,
    ActionItemUpdateResponse,
    ErrorResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/action-items",
    tags=["action-items"],
    responses={
        404: {"model": ErrorResponse, "description": "Action item not found"},
        500: {"model": ErrorResponse, "description": "Database error"},
    },
)


@router.post(
    "/extract-llm",
    response_model=ActionItemExtractResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract action items using LLM",
    description="Extract action items from free-form text using an LLM (Ollama)",
)
def extract_llm(payload: ActionItemExtractRequest) -> ActionItemExtractResponse:
    """
    Extract action items from text using LLM.
    
    Uses Ollama to extract action items with semantic understanding,
    providing better results than simple heuristics for complex text.
    
    Args:
        payload: Extraction request with text and save_note flag
        
    Returns:
        Extraction results with action items and optional note ID
        
    Raises:
        HTTPException: If extraction or database operations fail
    """
    try:
        note_id: Optional[int] = None
        
        # Save as note if requested
        if payload.save_note:
            note_id = db.insert_note(payload.text)
            logger.info(f"Saved note with ID: {note_id}")
        
        # Extract action items using LLM
        items = extract_action_items_llm(payload.text)
        
        # Save action items to database
        if items:
            ids = db.insert_action_items(items, note_id=note_id)
            logger.info(f"LLM extracted {len(items)} action items")
        else:
            ids = []
            logger.info("LLM found no action items")
        
        return ActionItemExtractResponse(
            note_id=note_id,
            items=[{"id": i, "text": t} for i, t in zip(ids, items)],
        )
    
    except ValueError as e:
        logger.warning(f"Invalid extraction request: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to extract action items with LLM: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract action items with LLM: {str(e)}",
        )


@router.post(
    "/extract",
    response_model=ActionItemExtractResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract action items from text",
    description="Extract action items from free-form text using heuristics",
)
def extract(payload: ActionItemExtractRequest) -> ActionItemExtractResponse:
    """
    Extract action items from text.
    
    Args:
        payload: Extraction request with text and save_note flag
        
    Returns:
        Extraction results with action items and optional note ID
        
    Raises:
        HTTPException: If extraction or database operations fail
    """
    try:
        note_id: Optional[int] = None
        
        # Save as note if requested
        if payload.save_note:
            note_id = db.insert_note(payload.text)
            logger.info(f"Saved note with ID: {note_id}")
        
        # Extract action items
        items = extract_action_items(payload.text)
        
        # Save action items to database
        if items:
            ids = db.insert_action_items(items, note_id=note_id)
            logger.info(f"Extracted {len(items)} action items")
        else:
            ids = []
            logger.info("No action items found")
        
        return ActionItemExtractResponse(
            note_id=note_id,
            items=[{"id": i, "text": t} for i, t in zip(ids, items)],
        )
    
    except ValueError as e:
        logger.warning(f"Invalid extraction request: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to extract action items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to extract action items",
        )


@router.get(
    "",
    response_model=List[ActionItemResponse],
    summary="List action items",
    description="List all action items, optionally filtered by note ID",
)
def list_all(
    note_id: Optional[int] = Query(None, description="Filter by note ID")
) -> List[ActionItemResponse]:
    """
    List action items, optionally filtered by note ID.
    
    Args:
        note_id: Optional note ID to filter by
        
    Returns:
        List of action items
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        rows = db.list_action_items(note_id=note_id)
        return [
            ActionItemResponse(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=bool(r["done"]),
                created_at=r["created_at"],
            )
            for r in rows
        ]
    except Exception as e:
        logger.error(f"Failed to list action items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve action items",
        )


@router.post(
    "/{action_item_id}/done",
    response_model=ActionItemUpdateResponse,
    summary="Update action item status",
    description="Mark an action item as done or not done",
)
def mark_done(
    action_item_id: int, payload: ActionItemUpdateRequest
) -> ActionItemUpdateResponse:
    """
    Update the completion status of an action item.
    
    Args:
        action_item_id: The action item ID to update
        payload: Update request with done status
        
    Returns:
        Updated action item status
        
    Raises:
        HTTPException: If action item not found or update fails
    """
    try:
        db.mark_action_item_done(action_item_id, payload.done)
        logger.info(f"Updated action item {action_item_id}: done={payload.done}")
        
        return ActionItemUpdateResponse(id=action_item_id, done=payload.done)
    
    except ActionItemNotFoundError as e:
        logger.warning(f"Action item not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Action item {action_item_id} not found",
        )
    except Exception as e:
        logger.error(f"Failed to update action item {action_item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update action item",
        )


