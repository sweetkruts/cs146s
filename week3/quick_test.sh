#!/bin/bash

# Quick test script for Spotify MCP Server

MCP_API_KEY="ZRQubh-q3TXz_-AEM0OvKalyqIb31KliGaHVvDe6gTM"
BASE_URL="http://127.0.0.1:8000"

echo "========================================="
echo "Spotify MCP Server - Quick Test"
echo "========================================="
echo ""

# Check auth status
echo "1. Checking authentication status..."
curl -s "$BASE_URL/auth/status" | python -m json.tool
echo ""

# List tools
echo "2. Listing available MCP tools..."
curl -s -X POST "$BASE_URL/mcp/list_tools" \
  -H "Authorization: Bearer $MCP_API_KEY" | python -m json.tool
echo ""

# Search for tracks
echo "3. Testing search_tracks (searching for 'Bohemian Rhapsody')..."
curl -s -X POST "$BASE_URL/mcp/call_tool" \
  -H "Authorization: Bearer $MCP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "search_tracks",
    "arguments": {
      "query": "Bohemian Rhapsody",
      "limit": 3
    }
  }' | python -m json.tool
echo ""

echo "========================================="
echo "Test complete!"
echo "========================================="

