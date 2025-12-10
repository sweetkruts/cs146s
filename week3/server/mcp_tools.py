from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.types as types
import logging
from .spotify_client import SpotifyClient

logger = logging.getLogger(__name__)

def register_tools(mcp_server: Server, spotify_client: SpotifyClient) -> None:
    """
    Register all MCP tools with the server.
    
    MCP Tool Structure:
    - name: Unique identifier the AI uses to call the tool
    - description: Tells the AI what the tool does and when to use it
    - inputSchema: JSON Schema defining required/optional parameters
    """
    
    @mcp_server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        MCP tool call handler.
        The AI sends tool name + arguments -> we execute and return results.
        """
        logger.info(f"Tool called: {name} with arguments: {arguments}")
        
        try:
            if name == "search_tracks":
                return await handle_search_tracks(spotify_client, arguments)
            elif name == "get_artist_info":
                return await handle_get_artist_info(spotify_client, arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")
        
        except ValueError as e:
            error_msg = f"Validation error: {str(e)}"
            logger.warning(error_msg)
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            error_msg = f"Error executing {name}: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return [TextContent(type="text", text=error_msg)]

def get_tool_definitions() -> List[Tool]:
    """
    Define all available MCP tools.
    
    Each tool has:
    1. name: What the AI calls
    2. description: What it does (helps AI decide when to use it)
    3. inputSchema: JSON Schema for parameters (enforces types/validation)
    """
    return [
        Tool(
            name="search_tracks",
            description=(
                "Search for songs on Spotify by name, artist, or keywords. "
                "Returns track details including name, artists, album, Spotify URL, "
                "and preview URL. Use this when the user wants to find specific songs "
                "or discover music matching certain criteria."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (song name, artist name, or keywords)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return (1-50)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    }
                },
                "required": ["query"]
            }
        ),
        
        Tool(
            name="get_artist_info",
            description=(
                "Get detailed information about a music artist including their name, "
                "genres, popularity score, follower count, top 5 tracks, and Spotify URL. "
                "Accepts either a Spotify artist ID or artist name (will search if name provided). "
                "Use this when the user asks about an artist, their music style, or wants to "
                "explore an artist's catalog."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "artist_name_or_id": {
                        "type": "string",
                        "description": "Artist name (e.g., 'Taylor Swift') or Spotify artist ID"
                    }
                },
                "required": ["artist_name_or_id"]
            }
        )
    ]

async def handle_search_tracks(spotify_client: SpotifyClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle search_tracks tool invocation."""
    query = arguments.get("query", "").strip()
    limit = arguments.get("limit", 10)
    
    if not query:
        return [TextContent(type="text", text="Error: 'query' parameter is required and cannot be empty")]
    
    tracks = spotify_client.search_tracks(query=query, limit=limit)
    
    if not tracks:
        return [TextContent(
            type="text",
            text=f"No tracks found for query: '{query}'"
        )]
    
    result_text = f"Found {len(tracks)} tracks for '{query}':\n\n"
    
    for i, track in enumerate(tracks, 1):
        artists_str = ", ".join(track['artists'])
        result_text += f"{i}. {track['name']} - {artists_str}\n"
        result_text += f"   Album: {track['album']}\n"
        result_text += f"   Popularity: {track['popularity']}/100\n"
        result_text += f"   Spotify: {track['spotify_url']}\n"
        result_text += f"   ID: {track['id']}\n"
        if track.get('preview_url'):
            result_text += f"   Preview: {track['preview_url']}\n"
        result_text += "\n"
    
    return [TextContent(type="text", text=result_text)]

async def handle_get_artist_info(spotify_client: SpotifyClient, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle get_artist_info tool invocation."""
    artist_name_or_id = arguments.get("artist_name_or_id", "").strip()
    
    if not artist_name_or_id:
        return [TextContent(type="text", text="Error: 'artist_name_or_id' parameter is required")]
    
    artist_info = spotify_client.get_artist_info(artist_name_or_id)
    
    result_text = f"Artist: {artist_info['name']}\n\n"
    result_text += f"Genres: {', '.join(artist_info['genres']) if artist_info['genres'] else 'N/A'}\n"
    result_text += f"Popularity: {artist_info['popularity']}/100\n"
    result_text += f"Followers: {artist_info['followers']:,}\n"
    result_text += f"Spotify: {artist_info['spotify_url']}\n"
    result_text += f"ID: {artist_info['id']}\n\n"
    
    result_text += "Top 5 Tracks:\n"
    for i, track in enumerate(artist_info['top_tracks'], 1):
        result_text += f"{i}. {track['name']} (from '{track['album']}')\n"
        result_text += f"   Popularity: {track['popularity']}/100\n"
    
    return [TextContent(type="text", text=result_text)]

