import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger("app.services.history_logger")

# Resolve history file path relative to the project root (3 levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
HISTORY_FILE = PROJECT_ROOT / "history.json"

def log_conversation(user_data: Dict[str, Any], themes: List[str], starters: List[str]) -> Dict[str, Any]:
    """
    Saves the generated session in history.json with a timestamp.
    """
    session = {
        "timestamp": datetime.now().isoformat(),
        "user": user_data,
        "themes": themes,
        "starters": starters
    }
    
    try:
        history = []
        if HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        history = json.loads(content)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error reading history file, resetting: {e}")
                history = []
                
        history.append(session)
        
        # Ensure directory exists (should be project root)
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
        return session
    except Exception as e:
        logger.error(f"Failed to log conversation to history: {e}")
        return session

def load_history() -> List[Dict[str, Any]]:
    """
    Loads all previous conversation sessions.
    """
    if not HISTORY_FILE.exists():
        return []
        
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        logger.error(f"Failed to load history: {e}")
        return []
