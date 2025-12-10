from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional
from .imessage_reader import Chat, Message


@dataclass
class StaleConversation:
    chat: Chat
    hours_since_last_message: float
    last_message_from_me: bool
    requires_followup: bool
    reason: str


class StaleDetector:
    def __init__(self, stale_threshold_hours: int = 48):
        self.stale_threshold_hours = stale_threshold_hours
    
    def analyze_conversations(self, chats: list[Chat]) -> list[StaleConversation]:
        now = datetime.now()
        stale_conversations = []
        
        for chat in chats:
            if not chat.last_message:
                continue
            
            time_diff = now - chat.last_message.date
            hours_since = time_diff.total_seconds() / 3600
            
            last_from_me = chat.last_message.is_from_me
            is_stale = hours_since >= self.stale_threshold_hours
            
            requires_followup = self._should_follow_up(
                is_stale=is_stale,
                last_from_me=last_from_me,
                hours_since=hours_since
            )
            
            reason = self._get_reason(
                is_stale=is_stale,
                last_from_me=last_from_me,
                hours_since=hours_since
            )
            
            stale_conversations.append(StaleConversation(
                chat=chat,
                hours_since_last_message=hours_since,
                last_message_from_me=last_from_me,
                requires_followup=requires_followup,
                reason=reason
            ))
        
        return [sc for sc in stale_conversations if sc.requires_followup]
    
    def _should_follow_up(self, is_stale: bool, last_from_me: bool, hours_since: float) -> bool:
        if not is_stale:
            return False
        
        if not last_from_me:
            return False
        
        return True
    
    def _get_reason(self, is_stale: bool, last_from_me: bool, hours_since: float) -> str:
        if not is_stale:
            return f"Recent activity ({hours_since:.1f}h ago)"
        
        if not last_from_me:
            return "Waiting for your response"
        
        return f"No reply to your message for {hours_since:.1f}h"
    
    def is_quiet_hours(self, quiet_start: int, quiet_end: int) -> bool:
        now = datetime.now()
        current_hour = now.hour
        
        if quiet_start < quiet_end:
            return quiet_start <= current_hour < quiet_end
        else:
            return current_hour >= quiet_start or current_hour < quiet_end




