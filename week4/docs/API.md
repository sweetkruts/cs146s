# API Reference

## Overview
REST API for the Developer Command Center application. Manages notes and action items.

## Base URL
http://localhost:8000

---

## Notes Endpoints

### List All Notes
**GET** `/notes/`

Returns all notes in the system.

**Response** (200):
```json
[
  {
    "id": 1,
    "title": "Example Note",
    "content": "Note content here"
  }
]
```

---

### Create Note
**POST** `/notes/`

Creates a new note.

**Request Body**:
```json
{
  "title": "string (required, 1-200 chars)",
  "content": "string (required, min 1 char)"
}
```

**Response** (201):
```json
{
  "id": 1,
  "title": "Example Note",
  "content": "Note content here"
}
```

**Error Responses**:
- 422: Validation error (missing or invalid fields)

---

### Search Notes
**GET** `/notes/search/`

Search for notes by title or content. Case-sensitive substring matching.

**Query Parameters**:
- `q` (string, optional): Search query. If omitted, returns all notes.

**Response** (200):
```json
[
  {
    "id": 1,
    "title": "Matching Note",
    "content": "Contains search query"
  }
]
```

---

### Get Note by ID
**GET** `/notes/{note_id}`

Retrieves a specific note by its ID.

**Path Parameters**:
- `note_id` (integer, required): ID of the note

**Response** (200):
```json
{
  "id": 1,
  "title": "Example Note",
  "content": "Note content here"
}
```

**Error Responses**:
- 404: Note not found

---

### Update Note
**PUT** `/notes/{note_id}`

Updates an existing note. Can update title, content, or both.

**Path Parameters**:
- `note_id` (integer, required): ID of the note to update

**Request Body**:
```json
{
  "title": "string (optional, 1-200 chars)",
  "content": "string (optional, min 1 char)"
}
```

At least one field must be provided.

**Response** (200):
```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Error Responses**:
- 404: Note not found
- 422: Validation error (invalid field values)

---

### Delete Note
**DELETE** `/notes/{note_id}`

Deletes a note permanently.

**Path Parameters**:
- `note_id` (integer, required): ID of the note to delete

**Response** (204):
Empty response body

**Error Responses**:
- 404: Note not found

---

## Action Items Endpoints

### List All Action Items
**GET** `/action-items/`

Returns all action items in the system.

**Response** (200):
```json
[
  {
    "id": 1,
    "description": "Complete assignment",
    "completed": false
  }
]
```

---

### Create Action Item
**POST** `/action-items/`

Creates a new action item. All items start as incomplete.

**Request Body**:
```json
{
  "description": "string (required, min 1 char)"
}
```

**Response** (201):
```json
{
  "id": 1,
  "description": "Complete assignment",
  "completed": false
}
```

**Error Responses**:
- 422: Validation error (missing or invalid fields)

---

### Complete Action Item
**PUT** `/action-items/{item_id}/complete`

Marks an action item as completed.

**Path Parameters**:
- `item_id` (integer, required): ID of the action item

**Response** (200):
```json
{
  "id": 1,
  "description": "Complete assignment",
  "completed": true
}
```

**Error Responses**:
- 404: Action item not found

---

## Status Codes

- **200 OK**: Successful GET or PUT request
- **201 Created**: Successful POST request
- **204 No Content**: Successful DELETE request
- **404 Not Found**: Resource doesn't exist
- **422 Unprocessable Entity**: Validation error

---

## Validation Rules

### Notes
- `title`: Must be 1-200 characters
- `content`: Must be at least 1 character

### Action Items
- `description`: Must be at least 1 character

---

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json



