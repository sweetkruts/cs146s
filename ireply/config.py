import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    IMESSAGE_DB_PATH: str = os.path.expanduser(
        os.getenv("IMESSAGE_DB_PATH", "~/Library/Messages/chat.db")
    )
    STALE_THRESHOLD_HOURS: int = int(os.getenv("STALE_THRESHOLD_HOURS", "48"))
    MAX_CONVERSATIONS_TO_CHECK: int = int(os.getenv("MAX_CONVERSATIONS_TO_CHECK", "20"))
    QUIET_HOURS_START: int = int(os.getenv("QUIET_HOURS_START", "22"))
    QUIET_HOURS_END: int = int(os.getenv("QUIET_HOURS_END", "8"))
    
    @classmethod
    def validate(cls) -> bool:
        if not cls.OPENAI_API_KEY:
            return False
        if not Path(cls.IMESSAGE_DB_PATH).exists():
            return False
        return True

