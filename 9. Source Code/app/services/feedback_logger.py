import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger("app.services.feedback_logger")

# Resolve feedback file path relative to the project root (3 levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FEEDBACK_FILE = PROJECT_ROOT / "feedback.json"

def log_feedback(suggestion: str, feedback: str, comment: Optional[str] = None) -> Dict[str, Any]:
    """
    Logs feedback for a conversation starter (like/dislike/suggestion).
    Saves the feedback details in feedback.json with a timestamp.
    """
    entry = {
        "suggestion": suggestion,
        "feedback": feedback,  # "like", "dislike", etc.
        "comment": comment or "",
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        feedback_list = []
        if FEEDBACK_FILE.exists():
            try:
                with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        feedback_list = json.loads(content)
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"Error reading feedback file, resetting: {e}")
                feedback_list = []
                
        feedback_list.append(entry)
        
        # Ensure directory exists (should be project root)
        FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(feedback_list, f, indent=2, ensure_ascii=False)
            
        return entry
    except Exception as e:
        logger.error(f"Failed to log feedback: {e}")
        return entry

def get_feedback() -> List[Dict[str, Any]]:
    """
    Retrieves all logged feedbacks.
    """
    if not FEEDBACK_FILE.exists():
        return []
        
    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        logger.error(f"Failed to retrieve feedback: {e}")
        return []
