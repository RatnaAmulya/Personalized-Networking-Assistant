import pytest
from app.services.event_analyzer import extract_event_themes

def test_extract_event_themes_default():
    """
    Verify that default candidate labels are used when candidate_labels is None,
    and returns a list of 3 strings.
    """
    desc = "A conference about Artificial Intelligence and machine learning in medicine."
    themes = extract_event_themes(desc)
    assert isinstance(themes, list)
    assert len(themes) == 3
    # Check that it identifies "Artificial Intelligence" or "Healthcare" or "Data Science"
    assert any(t in ["Artificial Intelligence", "Healthcare", "Data Science"] for t in themes)

def test_extract_event_themes_custom():
    """
    Verify that custom candidate labels are correctly scored and filtered.
    """
    desc = "Learning about bitcoin, ethereum, and smart contract security."
    candidates = ["Finance", "Blockchain & Web3", "Education", "Cybersecurity"]
    themes = extract_event_themes(desc, candidate_labels=candidates)
    assert isinstance(themes, list)
    assert len(themes) <= 3
    # Verify top themes match the context
    assert "Blockchain & Web3" in themes or "Cybersecurity" in themes

def test_extract_event_themes_empty():
    """
    Verify behavior with an empty description.
    """
    themes = extract_event_themes("")
    assert isinstance(themes, list)
    assert len(themes) == 3
