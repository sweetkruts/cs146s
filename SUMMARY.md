# iReply: Project Summary

## Problem Statement

In today's fast-paced digital communication, it's easy to lose track of messages that need responses. People often forget to reply to important texts, leading to missed opportunities, strained relationships, and general communication breakdown. iReply addresses this problem by automatically detecting stale conversations and helping users craft appropriate follow-up messages.

## Solution

iReply is an intelligent iMessage follow-up agent that:

1. **Reads your iMessage database** directly from macOS
2. **Detects two types of stale conversations**:
   - Messages from others you haven't replied to
   - Your messages that haven't received a response
3. **Generates contextual AI-powered drafts** using GPT-4o
4. **Sends messages** directly through iMessage via AppleScript

## Technical Implementation

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│  FastAPI Server │────▶│  iMessage DB    │
│   (Frontend)    │◀────│  (web_app.py)   │◀────│  (SQLite)       │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐     ┌─────────────────┐
                        │   GPT-4o API    │     │   AppleScript   │
                        │ (Draft Gen)     │     │   (Send Msg)    │
                        └─────────────────┘     └─────────────────┘
```

### Key Components

| Component | File | Purpose |
|-----------|------|---------|
| Web Server | `web_app.py` | FastAPI REST API serving the frontend |
| iMessage Reader | `ireply/imessage_reader.py` | SQLite interface to chat.db |
| Stale Detector | `ireply/stale_detector.py` | Conversation analysis logic |
| Draft Generator | `ireply/draft_generator.py` | GPT-4o prompt engineering |
| Message Sender | `ireply/message_sender.py` | AppleScript iMessage integration |
| Frontend | `static/` | HTML/CSS/JS web interface |

### Technical Challenges Solved

1. **Apple Timestamp Conversion**: iMessage uses nanoseconds since January 1, 2001 (Apple epoch). We convert this to standard Unix timestamps for accurate time calculations.

2. **Attributed Body Extraction**: Newer iOS versions store message text in binary `attributedBody` blobs instead of plain `text` columns. We implemented a regex-based extractor to parse these blobs.

3. **Context-Aware Prompting**: The AI generates different follow-ups based on conversation context, message history, and whether it's a 1:1 or group chat.

## Features

### Implemented
- ✅ Real-time iMessage database reading
- ✅ Two-way stale detection (need to reply / waiting for reply)
- ✅ Configurable time threshold (0-720 hours)
- ✅ GPT-4o powered draft generation
- ✅ Context analysis (last 10 messages)
- ✅ Direct message sending via AppleScript
- ✅ Modern web interface with dark theme
- ✅ Group chat vs 1:1 detection

### Future Enhancements
- Background monitoring daemon
- Native macOS menu bar app
- Draft history and learning
- Contact name resolution from Contacts.app
- Do-not-disturb scheduling

## Code Statistics

| Metric | Count |
|--------|-------|
| Python Files | 7 |
| Lines of Python | ~600 |
| Frontend Files | 3 (HTML, CSS, JS) |
| Lines of Frontend | ~700 |
| API Endpoints | 5 |
| Dependencies | 5 (openai, fastapi, uvicorn, rich, python-dotenv) |

## AI Tools Used

### Development
- **Cursor IDE with Claude**: Primary development environment for code generation, debugging, and refactoring
- **GitHub Copilot**: Code completion and suggestions

### Runtime
- **GPT-4o (OpenAI)**: Generates contextual follow-up message drafts based on conversation history

### AI Tool Reflection

**What worked well:**
- Rapid prototyping of the SQLite database queries
- FastAPI boilerplate and endpoint structure
- CSS styling and responsive design
- Debugging timestamp conversion issues

**Challenges:**
- Initial timestamp conversion was incorrect; required understanding Apple's epoch
- Binary plist parsing for attributedBody required iterative refinement
- Prompt engineering for natural-sounding drafts took multiple iterations

## Demo Instructions

1. Ensure macOS with iMessage configured
2. Grant Full Disk Access to Terminal
3. Set OpenAI API key in `.env`
4. Run `make web` and open http://localhost:8000
5. Set threshold to 0 to see all conversations
6. Click "Scan Conversations"
7. Click "Generate Reply" or "Generate Follow-up" on any card
8. Review draft and click "Send via iMessage"

## Conclusion

iReply demonstrates practical application of AI in personal productivity tools. By combining local database access, LLM-powered text generation, and native OS integration, we created a useful tool that helps users maintain better communication habits. The project showcases modern web development practices, API design, and thoughtful AI integration.

---

*CS146S Final Project — William Li & Gerwin Mateo — Stanford University, Fall 2024*



