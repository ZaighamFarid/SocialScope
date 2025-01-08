"""
request_model.py

Defines the structure of incoming API requests
"""

from pydantic import BaseModel, HttpUrl, Field
from enum import Enum

class CommentTone(str, Enum):
    """Available tone options for comment generation"""
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    FUNNY = "funny"
    SUPPORTIVE = "supportive"

class AnalyzeRequest(BaseModel):
    """
    Request payload for post analysis
    
    Fields:
        url: The social media post URL to analyze
        tone: Preferred tone for the suggested comment
    """
    url: str = Field(..., description="URL of the social media post to analyze")
    tone: CommentTone = Field(
        default=CommentTone.FRIENDLY,
        description="Tone for the AI-generated comment"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://twitter.com/user/status/12345",
                "tone": "friendly"
            }
        }
