#!/usr/bin/env python3
"""
iReply Web API Server
FastAPI backend for the iReply web frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import uvicorn

from ireply.config import Config
from ireply.imessage_reader import iMessageReader
from ireply.stale_detector import StaleDetector
from ireply.draft_generator import DraftGenerator
from ireply.message_sender import MessageSender


app = FastAPI(title="iReply API", version="1.0.0")

# Initialize components
reader = None
detector = None
generator = None
sender = None


def get_components():
    global reader, detector, generator, sender
    if reader is None:
        reader = iMessageReader(Config.IMESSAGE_DB_PATH)
        detector = StaleDetector(Config.STALE_THRESHOLD_HOURS)
        generator = DraftGenerator(Config.OPENAI_API_KEY)
        sender = MessageSender()
    return reader, detector, generator, sender


# Request/Response models
class GenerateDraftRequest(BaseModel):
    chat_id: int
    contact: str


class GenerateDraftResponse(BaseModel):
    draft: str
    context_messages: int


class SendMessageRequest(BaseModel):
    recipient: str
    message: str


class SendMessageResponse(BaseModel):
    success: bool
    error: str | None = None


class ConversationResponse(BaseModel):
    chat_id: int
    contact: str
    contact_name: str | None = None
    last_message: str
    hours_ago: float
    is_group: bool
    context_count: int


# API Endpoints
@app.get("/api/conversations", response_model=list[ConversationResponse])
async def get_stale_conversations(threshold: int = None):
    """Get all stale conversations needing follow-up (you sent last message)"""
    try:
        reader, detector, _, _ = get_components()
        
        # Use custom threshold if provided
        if threshold is not None:
            detector = StaleDetector(threshold)
        
        chats = reader.get_recent_chats(limit=Config.MAX_CONVERSATIONS_TO_CHECK)
        stale_convos = detector.analyze_conversations(chats)
        
        results = []
        for stale in stale_convos:
            chat = stale.chat
            contact = chat.display_name or chat.chat_identifier
            contact_name = reader.get_contact_name(chat.chat_identifier)
            last_msg = chat.last_message.text if chat.last_message else "[media]"
            if last_msg and len(last_msg) > 60:
                last_msg = last_msg[:57] + "..."
            
            # Get context count
            history = reader.get_chat_history(chat.chat_id, limit=10)
            text_count = sum(1 for msg in history if msg.text and len(msg.text) > 5)
            
            results.append(ConversationResponse(
                chat_id=chat.chat_id,
                contact=contact,
                contact_name=contact_name,
                last_message=last_msg or "[media/reaction]",
                hours_ago=round(stale.hours_since_last_message, 1),
                is_group=len(chat.participants) > 1,
                context_count=text_count
            ))
        
        return results
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail="iMessage database not accessible. Grant Full Disk Access to Terminal.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/need-to-reply", response_model=list[ConversationResponse])
async def get_need_to_reply(threshold: int = None):
    """Get conversations where others are waiting for your reply"""
    try:
        reader, _, _, _ = get_components()
        from datetime import datetime
        
        # Use custom threshold or default to 0 (show all)
        min_hours = threshold // 4 if threshold else 0
        
        chats = reader.get_recent_chats(limit=Config.MAX_CONVERSATIONS_TO_CHECK)
        now = datetime.now()
        
        results = []
        for chat in chats:
            if not chat.last_message:
                continue
            
            # Only include if last message is NOT from me (they're waiting for my reply)
            if chat.last_message.is_from_me:
                continue
            
            time_diff = now - chat.last_message.date
            hours_since = time_diff.total_seconds() / 3600
            
            # Only show if it's been at least min_hours
            if hours_since < min_hours:
                continue
            
            contact = chat.display_name or chat.chat_identifier
            contact_name = reader.get_contact_name(chat.chat_identifier)
            last_msg = chat.last_message.text if chat.last_message else "[media]"
            if last_msg and len(last_msg) > 60:
                last_msg = last_msg[:57] + "..."
            
            history = reader.get_chat_history(chat.chat_id, limit=10)
            text_count = sum(1 for msg in history if msg.text and len(msg.text) > 5)
            
            results.append(ConversationResponse(
                chat_id=chat.chat_id,
                contact=contact,
                contact_name=contact_name,
                last_message=last_msg or "[media/reaction]",
                hours_ago=round(hours_since, 1),
                is_group=len(chat.participants) > 1,
                context_count=text_count
            ))
        
        # Sort by hours_ago descending (oldest first - most urgent)
        results.sort(key=lambda x: x.hours_ago, reverse=True)
        
        return results
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail="iMessage database not accessible. Grant Full Disk Access to Terminal.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-draft", response_model=GenerateDraftResponse)
async def generate_draft(request: GenerateDraftRequest):
    """Generate an AI-powered follow-up draft for a conversation"""
    try:
        reader, _, generator, _ = get_components()
        
        # Get chat and history
        chats = reader.get_recent_chats(limit=100)
        target_chat = None
        for chat in chats:
            if chat.chat_id == request.chat_id:
                target_chat = chat
                break
        
        if not target_chat:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        history = reader.get_chat_history(request.chat_id, limit=10)
        hours_since = 0
        if target_chat.last_message:
            time_diff = datetime.now() - target_chat.last_message.date
            hours_since = time_diff.total_seconds() / 3600
        
        draft = generator.generate_followup(
            chat=target_chat,
            conversation_history=history,
            hours_since_last=hours_since
        )
        
        text_count = sum(1 for msg in history if msg.text and len(msg.text) > 5)
        
        return GenerateDraftResponse(
            draft=draft,
            context_messages=text_count
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/send-message", response_model=SendMessageResponse)
async def send_message(request: SendMessageRequest):
    """Send a message via iMessage"""
    try:
        _, _, _, sender = get_components()
        
        # Test connection first
        can_send, error = sender.test_connection()
        if not can_send:
            return SendMessageResponse(success=False, error=f"Messages app not accessible: {error}")
        
        # Send the message
        success, error = sender.send_message(request.recipient, request.message)
        
        return SendMessageResponse(success=success, error=error)
    
    except Exception as e:
        return SendMessageResponse(success=False, error=str(e))


@app.get("/api/health")
async def health_check():
    """Check if the API is running and configured"""
    has_api_key = bool(Config.OPENAI_API_KEY)
    db_exists = False
    try:
        from pathlib import Path
        db_exists = Path(Config.IMESSAGE_DB_PATH).exists()
    except:
        pass
    
    return {
        "status": "ok",
        "api_key_configured": has_api_key,
        "database_accessible": db_exists,
        "stale_threshold_hours": Config.STALE_THRESHOLD_HOURS
    }


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")


if __name__ == "__main__":
    print("\n🚀 Starting iReply Web Server...")
    print("   Open http://localhost:8000 in your browser\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

