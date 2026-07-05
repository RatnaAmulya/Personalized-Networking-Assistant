import pytest
from unittest.mock import patch, MagicMock
from app.services.fact_checker import fact_check

@patch('app.services.fact_checker.requests.get')
def test_fact_check_success(mock_get):
    """
    Test successful Wikipedia page summary lookup.
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "extract": "Artificial intelligence (AI) is intelligence demonstrated by machines.",
        "content_urls": {
            "desktop": {
                "page": "https://en.wikipedia.org/wiki/Artificial_intelligence"
            }
        }
    }
    mock_get.return_value = mock_resp
    
    result = fact_check("Artificial Intelligence")
    
    assert result["status"] == "Verified"
    assert "intelligence demonstrated by machines" in result["summary"]
    assert result["wikipedia_url"] == "https://en.wikipedia.org/wiki/Artificial_intelligence"
    assert result["topic"] == "Artificial Intelligence"

@patch('app.services.fact_checker.requests.get')
def test_fact_check_not_found(mock_get):
    """
    Test when page is not found directly and fallback search yields no results.
    """
    mock_resp_404 = MagicMock()
    mock_resp_404.status_code = 404
    
    # Second search mock response
    mock_search_resp = MagicMock()
    mock_search_resp.status_code = 200
    mock_search_resp.json.return_value = ["nonexistent_query", [], [], []]
    
    mock_get.side_effect = [mock_resp_404, mock_search_resp]
    
    result = fact_check("nonexistent_query")
    assert result["status"] == "Not Found"
    assert "could not find a page" in result["summary"]

@patch('app.services.fact_checker.requests.get')
def test_fact_check_exception(mock_get):
    """
    Test that connection failures return a graceful status and error message.
    """
    mock_get.side_effect = Exception("Connection Timeout")
    
    result = fact_check("Blockchain")
    assert result["status"] == "Connection Error"
    assert "Failed to connect" in result["summary"]
