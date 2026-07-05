import pytest
from app.schemas import UserProfile, EventContext
from app.services.topic_generator import generate_topics

@pytest.fixture
def sample_profile():
    return UserProfile(
        name="Alex Smith",
        bio="Full stack developer passionate about decentralized finance.",
        skills=["Python", "Solidity", "Docker"],
        interests=["Web3", "Finance", "Sailing"],
        profession="Software Engineer",
        company="CryptoCore Ltd",
        experience="Senior",
        goals="Find software partners and co-founders."
    )

@pytest.fixture
def sample_event():
    return EventContext(
        event_name="Decentralized Tech Summit",
        event_description="Annual meetup for developers and investors in blockchain technologies.",
        event_themes=["Blockchain & Web3", "Finance & Fintech"],
        event_type="Meetup"
    )

def test_generate_topics_count(sample_profile, sample_event):
    """
    Verify that generating topics returns exactly 5 starters.
    """
    themes = ["Blockchain & Web3", "Finance & Fintech"]
    starters = generate_topics(sample_profile, sample_event, themes)
    assert isinstance(starters, list)
    assert len(starters) == 5

def test_generate_topics_personalization(sample_profile, sample_event):
    """
    Verify that generated starters contain profile name and companies/themes.
    """
    themes = ["Blockchain & Web3", "Finance & Fintech"]
    starters = generate_topics(sample_profile, sample_event, themes)
    
    # Check that the templates contain the user's name
    has_name = any(sample_profile.name in s for s in starters)
    assert has_name, "User's name should be present in at least some templates"
    
    # Check that themes are present in the starters
    has_theme = any("Blockchain & Web3" in s or "Finance" in s for s in starters)
    assert has_theme, "Themes should be present in the starters"
