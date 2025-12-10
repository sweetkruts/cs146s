"""
Database layer with improved error handling and configuration.

Provides a clean abstraction over SQLite with proper error handling,
connection management, and configuration support.
"""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional

from .config import settings

# Configure logging
logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Base exception for database-related errors."""

    pass


class NoteNotFoundError(DatabaseError):
    """Raised when a note is not found."""

    pass


class ActionItemNotFoundError(DatabaseError):
    """Raised when an action item is not found."""

    pass


def ensure_data_directory_exists() -> None:
    """Ensure the data directory exists."""
    data_dir = settings.get_data_dir()
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Data directory ensured at: {data_dir}")
    except OSError as e:
        raise DatabaseError(f"Failed to create data directory: {e}") from e


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager for database connections.
    
    Ensures proper connection handling with automatic commit/rollback.
    Usage:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(...)
    """
    ensure_data_directory_exists()
    db_path = settings.get_database_path()
    
    connection = None
    try:
        connection = sqlite3.connect(str(db_path))
        connection.row_factory = sqlite3.Row
        logger.debug(f"Database connection opened: {db_path}")
        yield connection
        connection.commit()
    except sqlite3.Error as e:
        if connection:
            connection.rollback()
            logger.error(f"Database error, transaction rolled back: {e}")
        raise DatabaseError(f"Database operation failed: {e}") from e
    finally:
        if connection:
            connection.close()
            logger.debug("Database connection closed")


def init_db() -> None:
    """
    Initialize the database schema.
    
    Creates tables if they don't exist. Safe to call multiple times.
    
    Raises:
        DatabaseError: If database initialization fails
    """
    ensure_data_directory_exists()
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            
            # Create notes table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT (datetime('now'))
                );
                """
            )
            
            # Create action_items table with foreign key constraint
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS action_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER,
                    text TEXT NOT NULL,
                    done INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT (datetime('now')),
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                );
                """
            )
            
            # Create indexes for better query performance
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_action_items_note_id 
                ON action_items(note_id);
                """
            )
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_action_items_done 
                ON action_items(done);
                """
            )
            
            logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def insert_note(content: str) -> int:
    """
    Insert a new note into the database.
    
    Args:
        content: The note content text
        
    Returns:
        The ID of the newly created note
        
    Raises:
        DatabaseError: If the insert operation fails
        ValueError: If content is empty
    """
    if not content or not content.strip():
        raise ValueError("Note content cannot be empty")
    
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content.strip(),))
            note_id = int(cursor.lastrowid)
            logger.info(f"Created note with ID: {note_id}")
            return note_id
    except Exception as e:
        logger.error(f"Failed to insert note: {e}")
        raise


def list_notes() -> list[sqlite3.Row]:
    """
    List all notes in descending order by ID.
    
    Returns:
        List of note rows
        
    Raises:
        DatabaseError: If the query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
            notes = list(cursor.fetchall())
            logger.debug(f"Retrieved {len(notes)} notes")
            return notes
    except Exception as e:
        logger.error(f"Failed to list notes: {e}")
        raise


def get_note(note_id: int) -> Optional[sqlite3.Row]:
    """
    Get a single note by ID.
    
    Args:
        note_id: The note ID to retrieve
        
    Returns:
        The note row if found, None otherwise
        
    Raises:
        DatabaseError: If the query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            if row:
                logger.debug(f"Retrieved note with ID: {note_id}")
            else:
                logger.debug(f"Note not found with ID: {note_id}")
            return row
    except Exception as e:
        logger.error(f"Failed to get note {note_id}: {e}")
        raise


def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    """
    Insert multiple action items into the database.
    
    Args:
        items: List of action item text strings
        note_id: Optional note ID to associate items with
        
    Returns:
        List of IDs for the newly created action items
        
    Raises:
        DatabaseError: If the insert operation fails
        ValueError: If items list is empty or contains empty strings
    """
    if not items:
        raise ValueError("Items list cannot be empty")
    
    # Filter out empty items
    valid_items = [item.strip() for item in items if item and item.strip()]
    if not valid_items:
        raise ValueError("No valid items to insert")
    
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            ids: list[int] = []
            for item in valid_items:
                cursor.execute(
                    "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                    (note_id, item),
                )
                ids.append(int(cursor.lastrowid))
            logger.info(f"Created {len(ids)} action items (note_id={note_id})")
            return ids
    except Exception as e:
        logger.error(f"Failed to insert action items: {e}")
        raise


def list_action_items(note_id: Optional[int] = None) -> list[sqlite3.Row]:
    """
    List action items, optionally filtered by note ID.
    
    Args:
        note_id: Optional note ID to filter by
        
    Returns:
        List of action item rows in descending order by ID
        
    Raises:
        DatabaseError: If the query fails
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            if note_id is None:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
                )
            else:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                    (note_id,),
                )
            items = list(cursor.fetchall())
            logger.debug(f"Retrieved {len(items)} action items (note_id={note_id})")
            return items
    except Exception as e:
        logger.error(f"Failed to list action items: {e}")
        raise


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    """
    Update the completion status of an action item.
    
    Args:
        action_item_id: The action item ID to update
        done: The new completion status
        
    Raises:
        DatabaseError: If the update operation fails
        ActionItemNotFoundError: If the action item doesn't exist
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            
            # Check if any row was updated
            if cursor.rowcount == 0:
                raise ActionItemNotFoundError(f"Action item {action_item_id} not found")
            
            logger.info(f"Updated action item {action_item_id}: done={done}")
    except ActionItemNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Failed to update action item {action_item_id}: {e}")
        raise


