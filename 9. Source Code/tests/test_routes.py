import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_read_root():
    """
    Test welcome endpoint GET /
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]
    assert response.json()["status"] == "online"

@patch("app.routers.conversation.extract_event_themes")
def test_analyze_event_route(mock_extract):
    """
    Test POST /analyze-event
    """
    mock_extract.return_value = ["AI", "Healthcare", "Education"]
    payload = {
        "event_description": "A networking event for AI developers in health tech.",
        "candidate_labels": ["AI", "Healthcare", "Education", "Marketing"]
    }
    response = client.post("/analyze-event", json=payload)
    assert response.status_code == 200
    assert response.json()["themes"] == ["AI", "Healthcare", "Education"]

@patch("app.routers.conversation.fact_check")
def test_fact_check_route(mock_fact_check):
    """
    Test POST /fact-check
    """
    mock_fact_check.return_value = {
        "topic": "Machine Learning",
        "summary": "Machine learning is a field of study in AI.",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Machine_learning",
        "status": "Verified"
    }
    payload = {"query": "Machine Learning"}
    response = client.post("/fact-check", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "Machine Learning"
    assert data["status"] == "Verified"

@patch("app.routers.conversation.extract_event_themes")
@patch("app.routers.conversation.generate_topics")
def test_generate_conversation_route(mock_generate, mock_extract):
    """
    Test POST /generate-conversation integration
    """
    mock_extract.return_value = ["AI", "Human Resources"]
    mock_generate.return_value = ["Starter 1", "Starter 2", "Starter 3", "Starter 4", "Starter 5"]
    
    payload = {
        "user_profile": {
            "name": "Jane",
            "bio": "Developer bio",
            "skills": ["Python"],
            "interests": ["Tech"],
            "profession": "Software Engineer",
            "company": "FastTech",
            "experience": "Senior",
            "goals": "Network"
        },
        "event_context": {
            "event_name": "Tech Meetup",
            "event_description": "Annual tech meetup for developers.",
            "event_themes": [],
            "event_type": "Meetup"
        }
    }
    response = client.post("/generate-conversation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["starters"]) == 5
    assert data["themes"] == ["AI", "Human Resources"]

def test_feedback_routes():
    """
    Test POST /feedback and GET /feedback
    """
    payload = {
        "suggestion": "How do you view AI shaping your field?",
        "feedback": "like",
        "comment": "Very natural icebreaker."
    }
    # Submit feedback
    post_resp = client.post("/feedback", json=payload)
    assert post_resp.status_code == 200
    assert post_resp.json()["feedback"] == "like"
    assert post_resp.json()["suggestion"] == payload["suggestion"]
    
    # Retrieve feedback
    get_resp = client.get("/feedback")
    assert get_resp.status_code == 200
    assert len(get_resp.json()) >= 1
    assert get_resp.json()[-1]["feedback"] == "like"

def test_history_route():
    """
    Test GET /history
    """
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
