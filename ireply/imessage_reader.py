import sqlite3
import subprocess
import re
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class Message:
    rowid: int
    text: Optional[str]
    handle_id: str
    is_from_me: bool
    date: datetime
    chat_id: int


@dataclass
class Chat:
    chat_id: int
    chat_identifier: str
    display_name: Optional[str]
    participants: list[str]
    last_message: Optional[Message]
    message_count: int


class iMessageReader:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise FileNotFoundError(f"iMessage database not found at {db_path}")
        self._contact_cache = {}
        self._load_contacts()
    
    def _load_contacts(self):
        """Load contacts from macOS AddressBook database."""
        try:
            import glob
            # Find the AddressBook database
            ab_paths = glob.glob(os.path.expanduser(
                "~/Library/Application Support/AddressBook/Sources/*/AddressBook-v22.abcddb"
            ))
            if not ab_paths:
                return
            
            conn = sqlite3.connect(f"file:{ab_paths[0]}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            # Get phone numbers with names
            cursor.execute("""
                SELECT ZFULLNUMBER, ZFIRSTNAME, ZLASTNAME 
                FROM ZABCDPHONENUMBER 
                JOIN ZABCDRECORD ON ZABCDPHONENUMBER.ZOWNER = ZABCDRECORD.Z_PK
                WHERE ZFULLNUMBER IS NOT NULL
            """)
            for row in cursor.fetchall():
                phone, first, last = row
                name = f"{first or ''} {last or ''}".strip()
                if name and phone:
                    normalized = self._normalize_phone(phone)
                    if normalized:
                        self._contact_cache[normalized] = name
            
            # Get emails with names
            cursor.execute("""
                SELECT ZADDRESS, ZFIRSTNAME, ZLASTNAME
                FROM ZABCDEMAILADDRESS
                JOIN ZABCDRECORD ON ZABCDEMAILADDRESS.ZOWNER = ZABCDRECORD.Z_PK
                WHERE ZADDRESS IS NOT NULL
            """)
            for row in cursor.fetchall():
                email, first, last = row
                name = f"{first or ''} {last or ''}".strip()
                if name and email:
                    self._contact_cache[email.lower()] = name
            
            conn.close()
        except Exception as e:
            pass  # Contacts unavailable
    
    @staticmethod
    def _normalize_phone(phone: str) -> str:
        """Normalize phone number for matching - extract just digits."""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        # Remove leading 1 for US numbers
        if len(digits) == 11 and digits.startswith('1'):
            digits = digits[1:]
        # Return last 10 digits for matching
        if len(digits) >= 10:
            return digits[-10:]
        return digits
    
    def get_contact_name(self, identifier: str) -> Optional[str]:
        """Look up contact name for phone/email."""
        if not identifier:
            return None
        # Try direct match (for emails)
        lower_id = identifier.lower().strip()
        if lower_id in self._contact_cache:
            return self._contact_cache[lower_id]
        # Try normalized phone (last 10 digits)
        normalized = self._normalize_phone(identifier)
        if normalized and normalized in self._contact_cache:
            return self._contact_cache[normalized]
        return None
    
    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(f"file:{self.db_path}?mode=ro", uri=True)
    
    def get_recent_chats(self, limit: int = 20) -> list[Chat]:
        conn = self._connect()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            c.ROWID as chat_id,
            c.chat_identifier,
            c.display_name,
            MAX(m.date) as last_message_date,
            COUNT(m.ROWID) as message_count
        FROM chat c
        LEFT JOIN chat_message_join cmj ON c.ROWID = cmj.chat_id
        LEFT JOIN message m ON cmj.message_id = m.ROWID
        WHERE c.chat_identifier IS NOT NULL
        GROUP BY c.ROWID
        ORDER BY last_message_date DESC
        LIMIT ?
        """
        
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        
        chats = []
        for row in rows:
            chat_id, chat_identifier, display_name, last_date, msg_count = row
            
            participants = self._get_chat_participants(cursor, chat_id)
            last_message = self._get_last_message(cursor, chat_id)
            
            chats.append(Chat(
                chat_id=chat_id,
                chat_identifier=chat_identifier,
                display_name=display_name,
                participants=participants,
                last_message=last_message,
                message_count=msg_count
            ))
        
        conn.close()
        return chats
    
    def _get_chat_participants(self, cursor: sqlite3.Cursor, chat_id: int) -> list[str]:
        query = """
        SELECT DISTINCT h.id
        FROM handle h
        JOIN chat_handle_join chj ON h.ROWID = chj.handle_id
        WHERE chj.chat_id = ?
        """
        cursor.execute(query, (chat_id,))
        return [row[0] for row in cursor.fetchall()]
    
    def _get_last_message(self, cursor: sqlite3.Cursor, chat_id: int) -> Optional[Message]:
        query = """
        SELECT 
            m.ROWID,
            m.text,
            m.attributedBody,
            COALESCE(h.id, 'me') as handle_id,
            m.is_from_me,
            m.date,
            ?
        FROM message m
        LEFT JOIN handle h ON m.handle_id = h.ROWID
        JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
        WHERE cmj.chat_id = ?
        ORDER BY m.date DESC
        LIMIT 1
        """
        cursor.execute(query, (chat_id, chat_id))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        rowid, text, attributed_body, handle_id, is_from_me, date_int, chat_id = row
        
        # Try to extract text from attributedBody if text is empty
        if not text and attributed_body:
            text = self._extract_text_from_attributed_body(attributed_body)
        
        date = self._convert_apple_timestamp(date_int)
        
        return Message(
            rowid=rowid,
            text=text,
            handle_id=handle_id,
            is_from_me=bool(is_from_me),
            date=date,
            chat_id=chat_id
        )
    
    @staticmethod
    def _extract_text_from_attributed_body(data: bytes) -> Optional[str]:
        """Extract plain text from attributedBody blob."""
        if not data:
            return None
        try:
            # The attributedBody is a binary plist containing NSAttributedString
            # Try to decode and find the actual message text
            text = data.decode('utf-8', errors='ignore')
            
            import re
            # Find readable text segments
            matches = re.findall(r'[\x20-\x7E\u00A0-\uFFFF]{2,}', text)
            if matches:
                # Filter out Apple/iMessage internal strings
                bad_patterns = [
                    'nsstring', 'nsmutablestring', 'nsattributed', 'nsobject', 
                    'streamtyped', 'nsvalue', 'nsdata', 'nsnumber', 'nsdictionary',
                    '__kim', '__cf', 'nscolor', 'nsfont', 'uicolor',
                    'attributename', 'fileTransferGUID', 'messagepartattribute',
                    'bplist', 'typedstream'
                ]
                filtered = [m for m in matches 
                           if len(m) > 1 
                           and not any(p in m.lower() for p in bad_patterns)
                           and not m.startswith('$')
                           and not re.match(r'^[A-F0-9\-]{8,}$', m)  # Filter GUIDs
                           and not re.match(r'^[\d\.\-\+]+$', m)]  # Filter pure numbers
                
                if filtered:
                    # Return the longest reasonable match (usually the actual message)
                    # But filter out very long strings (likely encoded data)
                    reasonable = [m for m in filtered if len(m) < 500]
                    if reasonable:
                        return max(reasonable, key=len)
            return None
        except:
            return None
    
    def get_chat_history(self, chat_id: int, limit: int = 10) -> list[Message]:
        conn = self._connect()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            m.ROWID,
            m.text,
            m.attributedBody,
            COALESCE(h.id, 'me') as handle_id,
            m.is_from_me,
            m.date,
            ?
        FROM message m
        LEFT JOIN handle h ON m.handle_id = h.ROWID
        JOIN chat_message_join cmj ON m.ROWID = cmj.message_id
        WHERE cmj.chat_id = ?
        ORDER BY m.date DESC
        LIMIT ?
        """
        
        cursor.execute(query, (chat_id, chat_id, limit))
        rows = cursor.fetchall()
        
        messages = []
        for row in rows:
            rowid, text, attributed_body, handle_id, is_from_me, date_int, chat_id = row
            
            # Try to extract text from attributedBody if text is empty
            if not text and attributed_body:
                text = self._extract_text_from_attributed_body(attributed_body)
            
            date = self._convert_apple_timestamp(date_int)
            
            messages.append(Message(
                rowid=rowid,
                text=text,
                handle_id=handle_id,
                is_from_me=bool(is_from_me),
                date=date,
                chat_id=chat_id
            ))
        
        conn.close()
        return list(reversed(messages))
    
    @staticmethod
    def _convert_apple_timestamp(timestamp: int) -> datetime:
        """Convert Apple's Core Data timestamp to datetime."""
        # Apple epoch is January 1, 2001 00:00:00 UTC
        # Unix epoch is January 1, 1970 00:00:00 UTC
        # Difference is 978307200 seconds
        APPLE_EPOCH_OFFSET = 978307200
        # Timestamp is in nanoseconds, convert to seconds and add offset
        unix_timestamp = (timestamp / 1_000_000_000) + APPLE_EPOCH_OFFSET
        return datetime.fromtimestamp(unix_timestamp)




