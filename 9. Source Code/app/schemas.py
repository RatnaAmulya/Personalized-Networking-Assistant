from pydantic import BaseModel, Field
from typing import List, Optional

class UserProfile(BaseModel):
    name: str = Field(..., description="User's full name")
    bio: str = Field(..., description="A short bio of the user")
    skills: List[str] = Field(..., description="List of user's skills")
    interests: List[str] = Field(..., description="List of user's personal/professional interests")
    profession: str = Field(..., description="User's profession or title")
    company: str = Field(..., description="User's current company")
    experience: str = Field(..., description="User's experience level or description")
    goals: str = Field(..., description="User's networking or professional goals")

class EventContext(BaseModel):
    event_name: str = Field(..., description="Name of the networking event")
    event_description: str = Field(..., description="Description of the event")
    event_themes: Optional[List[str]] = Field(default=None, description="Known themes of the event")
    event_type: str = Field(..., description="Type of the event (e.g., Conference, Meetup, Panel)")

class ConversationRequest(BaseModel):
    user_profile: UserProfile = Field(..., description="The user's profile details")
    event_context: EventContext = Field(..., description="The context of the event")

class ConversationResponse(BaseModel):
    themes: List[str] = Field(..., description="Extracted themes from the event description")
    starters: List[str] = Field(..., description="Generated 5 personalized conversation starters")

class ThemeAnalysisRequest(BaseModel):
    event_description: str = Field(..., description="The description of the event to analyze")
    candidate_labels: Optional[List[str]] = Field(default=None, description="Optional labels for classification")

class ThemeAnalysisResponse(BaseModel):
    themes: List[str] = Field(..., description="Extracted top themes")

class FactCheckRequest(BaseModel):
    query: str = Field(..., description="The networking topic to verify on Wikipedia")

class FactCheckResponse(BaseModel):
    topic: str = Field(..., description="The checked query/topic")
    summary: str = Field(..., description="Summary from Wikipedia")
    wikipedia_url: str = Field(..., description="Wikipedia article URL")
    status: str = Field(..., description="Status of the verification (e.g., Verified, Not Found, Error)")
