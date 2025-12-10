# Quick Start Guide

## 5-Minute Setup

### 1. Get Spotify Credentials (2 min)
1. Go to https://developer.spotify.com/dashboard
2. Create app, add redirect: `http://127.0.0.1:8000/auth/callback` (**NOT localhost**)
3. Copy Client ID and Secret

### 2. Configure (1 min)
```bash
cd week3
cp .env.example .env
# Edit .env with your credentials
python -c "import secrets; print(secrets.token_urlsafe(32))"  # Generate MCP_API_KEY
```

### 3. Install & Run (2 min)
```bash
pip install -r requirements.txt
python -m server.main
```

Server starts at: http://localhost:8000

### 4. Authenticate
Visit: http://localhost:8000/auth/login

### 5. Test
```bash
python test_client.py
```

## Quick Test with curl

```bash
# Set your MCP API key
export MCP_KEY="your_mcp_api_key"

# Search tracks
curl -X POST http://localhost:8000/mcp/call_tool \
  -H "Authorization: Bearer $MCP_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "search_tracks",
    "arguments": {"query": "Radiohead", "limit": 3}
  }'
```

## Common Issues

**"Configuration error"** → Check `.env` has real values (not placeholders)

**"Not authenticated"** → Visit `/auth/login` first

**"Invalid redirect URI"** → Must be exactly `http://127.0.0.1:8000/auth/callback` in Spotify Dashboard (NOT localhost)

## Files Overview

- `server/main.py` - HTTP server & OAuth2 endpoints
- `server/spotify_client.py` - Spotify API wrapper
- `server/mcp_tools.py` - MCP tool definitions
- `test_client.py` - Automated test suite
- `example_ai_client.py` - AI integration example

## MCP Tools

1. **search_tracks** - Find songs by query
2. **get_artist_info** - Get artist details & top tracks

## Next Steps

- Read full [README.md](README.md) for details
- Try `example_ai_client.py` for workflow examples
- Integrate with Claude/GPT API
- Deploy remotely (optional)

**Note:** Server has 2 fully-working MCP tools (meets 2+ requirement)

