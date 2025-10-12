from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types
import logging
import sys
from typing import Optional
from contextlib import asynccontextmanager

from .config import settings
from .spotify_client import SpotifyClient
from .mcp_tools import register_tools, get_tool_definitions

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

spotify_client: Optional[SpotifyClient] = None
mcp_server: Optional[Server] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown lifecycle.
    Initialize Spotify client and MCP server on startup.
    """
    global spotify_client, mcp_server
    
    logger.info("Starting Spotify MCP Server...")
    
    try:
        settings.validate_config()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    
    spotify_client = SpotifyClient(
        client_id=settings.spotify_client_id,
        client_secret=settings.spotify_client_secret,
        redirect_uri=settings.spotify_redirect_uri
    )
    
    mcp_server = Server("spotify-mcp-server")
    
    @mcp_server.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available MCP tools."""
        return get_tool_definitions()
    
    register_tools(mcp_server, spotify_client)
    
    logger.info("Server initialized successfully")
    
    yield
    
    logger.info("Shutting down Spotify MCP Server...")

app = FastAPI(
    title="Spotify MCP Server",
    description="Model Context Protocol server wrapping Spotify Web API with OAuth2",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_mcp_api_key(authorization: Optional[str] = Header(None)) -> bool:
    """
    Middleware to validate MCP API key.
    
    Security for MCP endpoints:
    - Clients must send: Authorization: Bearer <MCP_API_KEY>
    - This is separate from Spotify OAuth2 (which authenticates users)
    - Prevents unauthorized access to the MCP server itself
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format. Use: Bearer <API_KEY>")
    
    token = authorization.replace("Bearer ", "")
    
    if token != settings.mcp_api_key:
        logger.warning("Invalid MCP API key attempt")
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return True

@app.get("/")
async def root():
    """Root endpoint with server info."""
    return {
        "name": "Spotify MCP Server",
        "version": "1.0.0",
        "status": "running",
        "authenticated": spotify_client.is_authenticated() if spotify_client else False,
        "endpoints": {
            "auth": "/auth/login",
            "status": "/auth/status",
            "mcp": "/mcp/*"
        }
    }

@app.get("/auth/login")
async def auth_login():
    """
    Spotify OAuth2 Step 1: Initiate authorization flow.
    
    Redirects user to Spotify's authorization page where they:
    1. Log in to their Spotify account
    2. Grant permissions to our app
    3. Get redirected back to /auth/callback
    """
    if not spotify_client:
        raise HTTPException(status_code=500, detail="Spotify client not initialized")
    
    auth_url = spotify_client.get_authorization_url()
    logger.info("Redirecting to Spotify authorization page")
    
    return RedirectResponse(url=auth_url)

@app.get("/auth/callback")
async def auth_callback(code: Optional[str] = None, error: Optional[str] = None):
    """
    Spotify OAuth2 Step 2: Handle callback and exchange code for tokens.
    
    After user authorizes, Spotify redirects here with:
    - code: temporary authorization code (if successful)
    - error: error message (if user denied)
    
    We exchange the code for access_token and refresh_token.
    """
    if error:
        logger.error(f"OAuth2 authorization error: {error}")
        return JSONResponse(
            status_code=400,
            content={"error": f"Authorization failed: {error}"}
        )
    
    if not code:
        return JSONResponse(
            status_code=400,
            content={"error": "No authorization code received"}
        )
    
    if not spotify_client:
        raise HTTPException(status_code=500, detail="Spotify client not initialized")
    
    try:
        token_info = spotify_client.exchange_code_for_token(code)
        logger.info("OAuth2 authorization successful")
        
        return JSONResponse(content={
            "status": "success",
            "message": "Successfully authenticated with Spotify!",
            "expires_in": token_info.get('expires_in', 3600)
        })
    
    except Exception as e:
        logger.error(f"Failed to exchange code for token: {e}")
        return JSONResponse(
            status_code=400,
            content={"error": f"Token exchange failed: {str(e)}"}
        )

@app.get("/auth/status")
async def auth_status():
    """Check if currently authenticated with Spotify."""
    if not spotify_client:
        return JSONResponse(content={"authenticated": False})
    
    is_auth = spotify_client.is_authenticated()
    
    return JSONResponse(content={
        "authenticated": is_auth,
        "message": "Authenticated with Spotify" if is_auth else "Not authenticated. Visit /auth/login"
    })

@app.post("/mcp/list_tools")
async def mcp_list_tools(authorized: bool = Depends(verify_mcp_api_key)):
    """
    MCP Endpoint: List available tools.
    
    Returns tool definitions (name, description, parameters) so the AI knows
    what capabilities are available.
    """
    if not spotify_client or not spotify_client.is_authenticated():
        raise HTTPException(
            status_code=401,
            detail="Not authenticated with Spotify. Complete OAuth2 flow first at /auth/login"
        )
    
    tools = get_tool_definitions()
    
    return JSONResponse(content={
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema
            }
            for tool in tools
        ]
    })

@app.post("/mcp/call_tool")
async def mcp_call_tool(request: Request, authorized: bool = Depends(verify_mcp_api_key)):
    """
    MCP Endpoint: Execute a tool.
    
    AI sends:
    - tool name
    - arguments (validated against inputSchema)
    
    We execute and return results.
    """
    if not spotify_client or not spotify_client.is_authenticated():
        raise HTTPException(
            status_code=401,
            detail="Not authenticated with Spotify. Complete OAuth2 flow first at /auth/login"
        )
    
    if not mcp_server:
        raise HTTPException(status_code=500, detail="MCP server not initialized")
    
    try:
        body = await request.json()
        tool_name = body.get("name")
        arguments = body.get("arguments", {})
        
        if not tool_name:
            raise HTTPException(status_code=400, detail="Tool name required")
        
        logger.info(f"MCP tool call: {tool_name} with args: {arguments}")
        
        from .mcp_tools import (
            handle_search_tracks,
            handle_get_artist_info
        )
        
        if tool_name == "search_tracks":
            result = await handle_search_tracks(spotify_client, arguments)
        elif tool_name == "get_artist_info":
            result = await handle_get_artist_info(spotify_client, arguments)
        else:
            raise HTTPException(status_code=404, detail=f"Tool not found: {tool_name}")
        
        return JSONResponse(content={
            "content": [{"type": "text", "text": item.text} for item in result]
        })
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing tool: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": f"Tool execution failed: {str(e)}"}
        )

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "spotify_authenticated": spotify_client.is_authenticated() if spotify_client else False
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting server with uvicorn...")
    uvicorn.run(
        "server.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

