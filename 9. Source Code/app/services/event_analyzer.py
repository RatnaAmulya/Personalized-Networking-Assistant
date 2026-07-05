import logging
from typing import List, Optional
from transformers import pipeline
from app.config import MODEL_NAMES

logger = logging.getLogger("app.services.event_analyzer")

# Global reference for the classifier (lazy loaded)
_classifier = None

def get_classifier():
    """
    Get or initialize the HuggingFace zero-shot classifier.
    Falls back to a keyword classifier if loading fails (e.g., offline or insufficient RAM).
    """
    global _classifier
    if _classifier is None:
        try:
            logger.info(f"Loading zero-shot classification model: {MODEL_NAMES['event_analysis']}")
            _classifier = pipeline(
                "zero-shot-classification",
                model=MODEL_NAMES["event_analysis"]
            )
        except Exception as e:
            logger.error(f"Failed to load model {MODEL_NAMES['event_analysis']}: {e}. Using rule-based fallback.")
            _classifier = "fallback"
    return _classifier

def extract_event_themes(description: str, candidate_labels: Optional[List[str]] = None) -> List[str]:
    """
    Extracts the top 3 event themes from the event description.
    """
    if not candidate_labels:
        candidate_labels = [
            "Artificial Intelligence", "Healthcare", "Blockchain & Web3", 
            "Education", "Sustainability & Green Tech", "Finance & Fintech", 
            "Marketing & Sales", "Human Resources", "Software Engineering",
            "Startup & Venture Capital", "Data Science", "Cybersecurity"
        ]
    
    if not description.strip():
        return candidate_labels[:3]

    classifier = get_classifier()
    
    if classifier == "fallback":
        # Basic matching logic for fallback
        desc_lower = description.lower()
        matched = []
        for label in candidate_labels:
            # Check if label or parts of label appear in the description
            words = label.lower().replace("&", "").split()
            if any(word in desc_lower for word in words if len(word) > 2):
                matched.append(label)
        
        # Ensure we have at least some themes
        if not matched:
            matched = candidate_labels[:3]
        return matched[:3]

    try:
        result = classifier(description, candidate_labels)
        return result["labels"][:3]
    except Exception as e:
        logger.error(f"Error during theme classification: {e}")
        # Return simple fallback
        desc_lower = description.lower()
        matched = [label for label in candidate_labels if label.lower() in desc_lower]
        return matched[:3] if matched else candidate_labels[:3]
