import subprocess
from typing import Optional


class MessageSender:
    """Send iMessages using AppleScript"""
    
    def __init__(self):
        pass
    
    def send_message(self, recipient: str, message: str) -> tuple[bool, Optional[str]]:
        """
        Send an iMessage to a recipient.
        
        Args:
            recipient: Phone number or email (e.g., "+19077648853" or "email@example.com")
            message: The message text to send
            
        Returns:
            tuple: (success: bool, error_message: Optional[str])
        """
        # Clean up the recipient
        recipient = recipient.strip()
        
        # Build AppleScript command
        applescript = f'''
        tell application "Messages"
            set targetService to 1st account whose service type = iMessage
            set targetBuddy to participant "{recipient}" of targetService
            send "{message}" to targetBuddy
        end tell
        '''
        
        try:
            # Execute AppleScript
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return (True, None)
            else:
                error = result.stderr.strip() if result.stderr else "Unknown error"
                return (False, error)
                
        except subprocess.TimeoutExpired:
            return (False, "AppleScript timeout - Messages app may not be responding")
        except Exception as e:
            return (False, f"Error sending message: {str(e)}")
    
    def test_connection(self) -> tuple[bool, Optional[str]]:
        """
        Test if Messages app is accessible.
        
        Returns:
            tuple: (success: bool, error_message: Optional[str])
        """
        applescript = '''
        tell application "Messages"
            return "connected"
        end tell
        '''
        
        try:
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return (True, None)
            else:
                return (False, "Messages app not accessible")
                
        except Exception as e:
            return (False, f"Error accessing Messages: {str(e)}")

