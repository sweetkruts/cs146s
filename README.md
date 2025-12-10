# iReply

**Intelligent iMessage Follow-up Agent** — A macOS application that helps you stay on top of your messages by detecting stale conversations and generating AI-powered follow-ups.

## Overview

iReply connects to your local iMessage database, analyzes your conversations, and uses GPT-4o to generate contextual follow-up messages. It features a modern web interface for easy interaction and can send messages directly through iMessage.

## Features

- **Stale Conversation Detection**: Identifies messages you haven't replied to and messages where you're waiting for a response
- **AI-Powered Drafts**: Uses GPT-4o to generate natural, context-aware follow-up messages
- **Direct iMessage Integration**: Reads from and sends to iMessage via macOS APIs
- **Configurable Threshold**: Set how many hours before a conversation is considered "stale"
- **Modern Web UI**: Clean, dark-themed interface for easy demo and daily use

## Requirements

- macOS 14+
- Python 3.10+
- OpenAI API key
- Full Disk Access permission for Terminal

## Quick Start

```bash
# 1. Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure API key
echo "OPENAI_API_KEY=your-key-here" > .env

# 3. Grant Full Disk Access to Terminal
# System Settings → Privacy & Security → Full Disk Access → Add Terminal

# 4. Start the web server
make web
```

Then open **http://localhost:8000** in your browser.

## Usage

1. **Set threshold**: Enter hours (0-720) to define when messages become "stale"
2. **Click "Scan Conversations"**: Loads messages from your iMessage database
3. **Review two sections**:
   - 📥 **Need to Reply**: Messages from others waiting for your response
   - 📤 **Waiting for Reply**: Your messages that haven't been answered
4. **Generate drafts**: Click to get AI-suggested follow-ups
5. **Edit and send**: Review the draft, edit if needed, then send via iMessage

## Project Structure

```
final-project/
├── web_app.py           # FastAPI web server
├── main.py              # CLI interface (alternative)
├── static/              # Web frontend
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── ireply/              # Core library
│   ├── config.py        # Configuration management
│   ├── imessage_reader.py   # iMessage database reader
│   ├── stale_detector.py    # Conversation analysis
│   ├── draft_generator.py   # GPT-4o integration
│   └── message_sender.py    # AppleScript message sender
├── requirements.txt
├── Makefile
└── env.template
```

## Configuration

Create a `.env` file with:

```bash
OPENAI_API_KEY=sk-...           # Required: OpenAI API key
STALE_THRESHOLD_HOURS=48        # Optional: Default threshold (hours)
MAX_CONVERSATIONS_TO_CHECK=20   # Optional: Number of chats to analyze
```

## Commands

```bash
make web      # Start web server (recommended)
make run      # Run CLI version
make install  # Install dependencies
make clean    # Remove cache files
```

## Team

- **William Li** (willyli@stanford.edu)
- **Gerwin Mateo** (gerwin08@stanford.edu)

CS146S: Modern Software Development — Stanford University, Fall 2024
