import time
import logging
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.schemas import (
    ConversationRequest, ConversationResponse,
    ThemeAnalysisRequest, ThemeAnalysisResponse,
    FactCheckRequest, FactCheckResponse
)
from app.services.event_analyzer import extract_event_themes
from app.services.topic_generator import generate_topics
from app.services.fact_checker import fact_check
from app.services.history_logger import log_conversation, load_history
from app.services.feedback_logger import log_feedback, get_feedback

logger = logging.getLogger("app.routers.conversation")
router = APIRouter()

# Input Pydantic model for saving feedback via API
class FeedbackSubmitRequest(BaseModel):
    suggestion: str = Field(..., description="The suggestion text that was rated")
    feedback: str = Field(..., description="The rating ('like' or 'dislike')")
    comment: Optional[str] = Field(default=None, description="Optional text comment/suggestion")

@router.post("/analyze-event", response_model=ThemeAnalysisResponse)
async def analyze_event(data: ThemeAnalysisRequest):
    """
    Extracts top event themes using the zero-shot classifier model.
    """
    start_time = time.time()
    logger.info("API request to /analyze-event initiated.")
    try:
        themes = extract_event_themes(data.event_description, data.candidate_labels)
        duration = time.time() - start_time
        logger.info(f"API request to /analyze-event completed in {duration:.4f}s. Themes: {themes}")
        return ThemeAnalysisResponse(themes=themes)
    except Exception as e:
        logger.error(f"Error in /analyze-event endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fact-check", response_model=FactCheckResponse)
async def run_fact_check(data: FactCheckRequest):
    """
    Verifies a networking topic using Wikipedia.
    """
    start_time = time.time()
    logger.info(f"API request to /fact-check initiated for query: '{data.query}'")
    try:
        result = fact_check(data.query)
        duration = time.time() - start_time
        logger.info(f"API request to /fact-check completed in {duration:.4f}s. Status: {result.get('status')}")
        return FactCheckResponse(
            topic=result["topic"],
            summary=result["summary"],
            wikipedia_url=result["wikipedia_url"],
            status=result["status"]
        )
    except Exception as e:
        logger.error(f"Error in /fact-check endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-conversation", response_model=ConversationResponse)
async def generate_conversation(data: ConversationRequest):
    """
    Full pipeline: Extracts themes, generates conversation starters, logs history, and returns results.
    """
    start_time = time.time()
    logger.info("API request to /generate-conversation initiated.")
    try:
        # Extract themes
        themes = extract_event_themes(data.event_context.event_description)
        
        # Generate starters
        starters = generate_topics(data.user_profile, data.event_context, themes)
        
        # Log to history (serialize user profile first)
        log_conversation(data.user_profile.model_dump(), themes, starters)
        
        duration = time.time() - start_time
        logger.info(f"API request to /generate-conversation completed in {duration:.4f}s. Starters count: {len(starters)}")
        return ConversationResponse(themes=themes, starters=starters)
    except Exception as e:
        logger.error(f"Error in /generate-conversation endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_history_api():
    """
    Retrieve all conversation history sessions.
    """
    start_time = time.time()
    logger.info("API request to /history initiated.")
    try:
        history = load_history()
        duration = time.time() - start_time
        logger.info(f"API request to /history completed in {duration:.4f}s. Total entries: {len(history)}")
        return history
    except Exception as e:
        logger.error(f"Error in /history endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback", response_model=Dict[str, Any])
async def submit_feedback_api(data: FeedbackSubmitRequest):
    """
    Submit user feedback for a starter.
    """
    start_time = time.time()
    logger.info(f"API post request to /feedback initiated for rating: {data.feedback}")
    try:
        result = log_feedback(data.suggestion, data.feedback, data.comment)
        duration = time.time() - start_time
        logger.info(f"API post request to /feedback completed in {duration:.4f}s.")
        return result
    except Exception as e:
        logger.error(f"Error in submit feedback API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback", response_model=List[Dict[str, Any]])
async def get_feedback_api():
    """
    Retrieve all logged feedback entries.
    """
    start_time = time.time()
    logger.info("API request to /feedback initiated.")
    try:
        feedback = get_feedback()
        duration = time.time() - start_time
        logger.info(f"API request to /feedback completed in {duration:.4f}s. Total entries: {len(feedback)}")
        return feedback
    except Exception as e:
        logger.error(f"Error in GET /feedback endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
