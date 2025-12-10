import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Dict, List, Optional, Any
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SpotifyClient:
    """
    Wrapper around Spotify Web API with OAuth2 Authorization Code Flow.
    
    OAuth2 Flow:
    1. User visits /auth/login -> redirected to Spotify authorization page
    2. User grants permission -> Spotify redirects back to /auth/callback with code
    3. Server exchanges code for access_token and refresh_token
    4. Access token used for API calls (expires in 1 hour)
    5. Refresh token used to get new access tokens without re-authentication
    """
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        
        self.sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-read-private user-read-email",
            cache_path=".spotify_cache"
        )
        
        self._sp_client: Optional[spotipy.Spotify] = None
        self._token_info: Optional[Dict[str, Any]] = None
        self._last_request_time = 0.0
        self.min_request_interval = 0.05
    
    def get_authorization_url(self) -> str:
        """Generate Spotify OAuth2 authorization URL."""
        return self.sp_oauth.get_authorize_url()
    
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token.
        Called after user authorizes and Spotify redirects to callback.
        """
        try:
            token_info = self.sp_oauth.get_access_token(code, as_dict=True, check_cache=False)
            self._token_info = token_info
            self._sp_client = spotipy.Spotify(auth=token_info['access_token'])
            logger.info("Successfully exchanged code for access token")
            return token_info
        except Exception as e:
            logger.error(f"Failed to exchange code for token: {e}")
            raise ValueError(f"OAuth2 error: {str(e)}")
    
    def is_authenticated(self) -> bool:
        """Check if we have a valid access token."""
        if not self._token_info:
            cached_token = self.sp_oauth.get_cached_token()
            if cached_token:
                self._token_info = cached_token
                self._sp_client = spotipy.Spotify(auth=cached_token['access_token'])
        
        return self._token_info is not None and not self._is_token_expired()
    
    def _is_token_expired(self) -> bool:
        """Check if current token is expired."""
        if not self._token_info:
            return True
        
        expires_at = self._token_info.get('expires_at', 0)
        return time.time() > expires_at
    
    def _refresh_token_if_needed(self) -> None:
        """Automatically refresh token if expired."""
        if self._is_token_expired() and self._token_info:
            try:
                logger.info("Access token expired, refreshing...")
                self._token_info = self.sp_oauth.refresh_access_token(
                    self._token_info['refresh_token']
                )
                self._sp_client = spotipy.Spotify(auth=self._token_info['access_token'])
                logger.info("Token refreshed successfully")
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                raise ValueError("Failed to refresh OAuth2 token. Please re-authenticate.")
    
    def _rate_limit_delay(self) -> None:
        """Simple rate limiting: ensure minimum time between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self._last_request_time = time.time()
    
    def _ensure_client(self) -> spotipy.Spotify:
        """Ensure we have an authenticated Spotify client."""
        if not self.is_authenticated():
            raise ValueError("Not authenticated. Please complete OAuth2 flow first.")
        
        self._refresh_token_if_needed()
        return self._sp_client
    
    def search_tracks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tracks on Spotify.
        
        Args:
            query: Search query (song name, artist, keywords)
            limit: Number of results (1-50)
        
        Returns:
            List of tracks with name, artist, album, URLs
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")
        
        if limit < 1 or limit > 50:
            raise ValueError("Limit must be between 1 and 50")
        
        sp = self._ensure_client()
        self._rate_limit_delay()
        
        try:
            results = sp.search(q=query, type='track', limit=limit)
            tracks = []
            
            for item in results['tracks']['items']:
                track = {
                    'id': item['id'],
                    'name': item['name'],
                    'artists': [artist['name'] for artist in item['artists']],
                    'album': item['album']['name'],
                    'spotify_url': item['external_urls']['spotify'],
                    'preview_url': item.get('preview_url'),
                    'duration_ms': item['duration_ms'],
                    'popularity': item['popularity']
                }
                tracks.append(track)
            
            logger.info(f"Search '{query}' returned {len(tracks)} tracks")
            return tracks
        
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                logger.warning("Rate limit hit, should implement backoff")
                raise ValueError("Rate limit exceeded. Please try again in a moment.")
            logger.error(f"Spotify API error during search: {e}")
            raise ValueError(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            raise ValueError(f"Search failed: {str(e)}")
    
    def get_artist_info(self, artist_name_or_id: str) -> Dict[str, Any]:
        """
        Get detailed information about an artist.
        
        Args:
            artist_name_or_id: Spotify artist ID or artist name to search
        
        Returns:
            Artist info including name, genres, popularity, top tracks
        """
        if not artist_name_or_id or not artist_name_or_id.strip():
            raise ValueError("Artist name or ID cannot be empty")
        
        sp = self._ensure_client()
        self._rate_limit_delay()
        
        try:
            if len(artist_name_or_id) == 22 and artist_name_or_id.isalnum():
                artist_id = artist_name_or_id
            else:
                search_results = sp.search(q=f"artist:{artist_name_or_id}", type='artist', limit=1)
                if not search_results['artists']['items']:
                    raise ValueError(f"No artist found matching '{artist_name_or_id}'")
                artist_id = search_results['artists']['items'][0]['id']
            
            artist = sp.artist(artist_id)
            top_tracks = sp.artist_top_tracks(artist_id, country='US')
            
            artist_info = {
                'id': artist['id'],
                'name': artist['name'],
                'genres': artist['genres'],
                'popularity': artist['popularity'],
                'followers': artist['followers']['total'],
                'spotify_url': artist['external_urls']['spotify'],
                'images': [img['url'] for img in artist['images']],
                'top_tracks': [
                    {
                        'name': track['name'],
                        'album': track['album']['name'],
                        'popularity': track['popularity'],
                        'preview_url': track.get('preview_url')
                    }
                    for track in top_tracks['tracks'][:5]
                ]
            }
            
            logger.info(f"Retrieved info for artist: {artist_info['name']}")
            return artist_info
        
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                raise ValueError("Rate limit exceeded. Please try again in a moment.")
            logger.error(f"Spotify API error getting artist: {e}")
            raise ValueError(f"Spotify API error: {str(e)}")
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting artist: {e}")
            raise ValueError(f"Failed to get artist info: {str(e)}")
    
    def get_recommendations(self, seed_track_ids: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get song recommendations based on seed tracks.
        
        Args:
            seed_track_ids: List of 1-5 Spotify track IDs to base recommendations on
            limit: Number of recommendations (1-100)
        
        Returns:
            List of recommended tracks with details
        """
        if not seed_track_ids or len(seed_track_ids) < 1:
            raise ValueError("Must provide at least 1 seed track")
        
        if len(seed_track_ids) > 5:
            raise ValueError("Maximum 5 seed tracks allowed")
        
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")
        
        sp = self._ensure_client()
        self._rate_limit_delay()
        
        try:
            recommendations = sp.recommendations(seed_tracks=seed_track_ids, limit=limit, market='US')
            
            rec_tracks = []
            for item in recommendations['tracks']:
                track = {
                    'id': item['id'],
                    'name': item['name'],
                    'artists': [artist['name'] for artist in item['artists']],
                    'album': item['album']['name'],
                    'spotify_url': item['external_urls']['spotify'],
                    'preview_url': item.get('preview_url'),
                    'popularity': item['popularity']
                }
                rec_tracks.append(track)
            
            logger.info(f"Generated {len(rec_tracks)} recommendations from {len(seed_track_ids)} seeds")
            return rec_tracks
        
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 429:
                raise ValueError("Rate limit exceeded. Please try again in a moment.")
            logger.error(f"Spotify API error getting recommendations: {e}")
            raise ValueError(f"Spotify API error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error getting recommendations: {e}")
            raise ValueError(f"Failed to get recommendations: {str(e)}")

