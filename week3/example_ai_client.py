#!/usr/bin/env python3
"""
Example: Using Spotify MCP Server with Claude AI

This demonstrates how an AI agent can use the MCP server to search
for music, get artist info, and generate recommendations.

Prerequisites:
1. Server running: python -m server.main
2. OAuth2 completed: http://localhost:8000/auth/login
3. Environment: pip install anthropic httpx python-dotenv

Usage:
  python example_ai_client.py
"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

MCP_API_KEY = os.getenv("MCP_API_KEY")
BASE_URL = "http://localhost:8000"

def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """
    Call an MCP tool and return the result.
    
    This is the bridge between AI and your MCP server.
    """
    headers = {
        "Authorization": f"Bearer {MCP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = httpx.post(
        f"{BASE_URL}/mcp/call_tool",
        headers=headers,
        json={"name": tool_name, "arguments": arguments},
        timeout=15
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['content'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

def example_workflow():
    """
    Example workflow: Search → Get Artist Info → Recommendations
    
    This simulates what an AI agent would do when asked:
    "Tell me about Daft Punk and recommend similar artists"
    """
    print("=" * 70)
    print("Example AI Workflow: Music Discovery")
    print("=" * 70)
    
    # Step 1: Search for Daft Punk tracks
    print("\n[AI] Searching for Daft Punk tracks...\n")
    search_result = call_mcp_tool(
        "search_tracks",
        {"query": "Daft Punk Get Lucky", "limit": 3}
    )
    print(search_result)
    
    # Step 2: Get artist information
    print("\n[AI] Getting Daft Punk artist info...\n")
    artist_result = call_mcp_tool(
        "get_artist_info",
        {"artist_name_or_id": "Daft Punk"}
    )
    print(artist_result)
    
    # Step 3: Get recommendations (using track ID from search)
    print("\n[AI] Generating recommendations based on 'Get Lucky'...\n")
    print("(Using track ID: 2Foc5Q5nqNiosCNqttzHof from search results)")
    
    recommendations = call_mcp_tool(
        "get_recommendations",
        {
            "seed_track_ids": ["2Foc5Q5nqNiosCNqttzHof"],
            "limit": 5
        }
    )
    print(recommendations)
    
    print("\n" + "=" * 70)
    print("Workflow Complete!")
    print("=" * 70)

def example_with_anthropic_sdk():
    """
    Example using Anthropic SDK (Claude) - requires anthropic package and API key.
    
    Uncomment and run if you have Claude API access.
    """
    print("\n\n💡 To use with Claude API:")
    print("""
    import anthropic
    
    client = anthropic.Anthropic(api_key="your_claude_api_key")
    
    tools = [
        {
            "name": "search_tracks",
            "description": "Search for songs on Spotify",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            }
        },
        # ... other tools
    ]
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=[{
            "role": "user",
            "content": "Find me some upbeat electronic music"
        }]
    )
    
    # If Claude wants to use a tool:
    if message.stop_reason == "tool_use":
        tool_use = message.content[-1]
        result = call_mcp_tool(tool_use.name, tool_use.input)
        
        # Send result back to Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=[
                {"role": "user", "content": "Find me some upbeat electronic music"},
                {"role": "assistant", "content": message.content},
                {
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result
                    }]
                }
            ]
        )
        
        print(response.content[0].text)
    """)

if __name__ == "__main__":
    try:
        example_workflow()
        example_with_anthropic_sdk()
        
        print("\n✓ Example completed successfully!")
        print("\nNext steps:")
        print("1. Try modifying the search queries")
        print("2. Experiment with different artists")
        print("3. Chain multiple tool calls together")
        print("4. Integrate with Claude/GPT API for real AI interactions")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("- Is the server running? (python -m server.main)")
        print("- Did you complete OAuth2? (visit /auth/login)")
        print("- Is MCP_API_KEY set in .env?")

