#!/usr/bin/env python3
"""
Simple test client to verify MCP server is working.

Usage:
1. Start the server: python -m server.main
2. Complete OAuth2 at: http://localhost:8000/auth/login
3. Run this script: python test_client.py
"""

import httpx
import json
import sys
from dotenv import load_dotenv
import os

load_dotenv()

MCP_API_KEY = os.getenv("MCP_API_KEY")
BASE_URL = "http://e:8000"

if not MCP_API_KEY:
    print("Error: MCP_API_KEY not found in .env file")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {MCP_API_KEY}",
    "Content-Type": "application/json"
}

def test_server_health():
    """Test basic server connectivity."""
    print("1. Testing server health...")
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=5)
        result = response.json()
        print(f"   ✓ Server is healthy")
        print(f"   Spotify authenticated: {result.get('spotify_authenticated', False)}")
        return result.get('spotify_authenticated', False)
    except Exception as e:
        print(f"   ✗ Server not reachable: {e}")
        print("   Make sure server is running: python -m server.main")
        return False

def test_auth_status():
    """Check Spotify authentication status."""
    print("\n2. Checking Spotify authentication...")
    try:
        response = httpx.get(f"{BASE_URL}/auth/status", timeout=5)
        result = response.json()
        if result.get('authenticated'):
            print(f"   ✓ {result.get('message')}")
            return True
        else:
            print(f"   ✗ {result.get('message')}")
            print(f"   Visit: {BASE_URL}/auth/login")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_list_tools():
    """Test MCP list_tools endpoint."""
    print("\n3. Testing MCP list_tools...")
    try:
        response = httpx.post(f"{BASE_URL}/mcp/list_tools", headers=headers, timeout=10)
        if response.status_code == 200:
            result = response.json()
            tools = result.get('tools', [])
            print(f"   ✓ Found {len(tools)} tools:")
            for tool in tools:
                print(f"     - {tool['name']}")
            return True
        else:
            print(f"   ✗ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_search_tracks():
    """Test search_tracks tool."""
    print("\n4. Testing search_tracks tool...")
    try:
        request = {
            "name": "search_tracks",
            "arguments": {
                "query": "Bohemian Rhapsody",
                "limit": 3
            }
        }
        response = httpx.post(f"{BASE_URL}/mcp/call_tool", headers=headers, json=request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            content = result.get('content', [])
            if content:
                print("   ✓ Search successful!")
                print("\n   Results:")
                print(content[0]['text'][:500] + "..." if len(content[0]['text']) > 500 else content[0]['text'])
                return True
        else:
            print(f"   ✗ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_get_artist_info():
    """Test get_artist_info tool."""
    print("\n5. Testing get_artist_info tool...")
    try:
        request = {
            "name": "get_artist_info",
            "arguments": {
                "artist_name_or_id": "Queen"
            }
        }
        response = httpx.post(f"{BASE_URL}/mcp/call_tool", headers=headers, json=request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            content = result.get('content', [])
            if content:
                print("   ✓ Artist info retrieved!")
                print("\n   Results:")
                print(content[0]['text'][:400] + "..." if len(content[0]['text']) > 400 else content[0]['text'])
                return True
        else:
            print(f"   ✗ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Spotify MCP Server Test Suite")
    print("=" * 60)
    
    if not test_server_health():
        print("\n❌ Server not running. Start it first!")
        sys.exit(1)
    
    if not test_auth_status():
        print("\n❌ Not authenticated. Visit /auth/login first!")
        sys.exit(1)
    
    results = []
    results.append(test_list_tools())
    results.append(test_search_tracks())
    results.append(test_get_artist_info())
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Server is working correctly.")
    else:
        print("✗ Some tests failed. Check errors above.")
    
    print("\n💡 To test get_recommendations, use track IDs from search_tracks results.")

if __name__ == "__main__":
    main()

