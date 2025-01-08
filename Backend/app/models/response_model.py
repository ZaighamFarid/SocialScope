"""
response_model.py

Defines the structure of API responses
"""

from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Sentiment(str, Enum):
    """Possible sentiment values"""
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"

class AnalyzeResponse(BaseModel):
    """
    Response payload containing analysis results
    
    Fields:
        summary: Condensed version of the post content
        sentiment: Overall emotional tone (Positive/Neutral/Negative)
        topics: Key themes or subjects mentioned in the post
        suggested_comment: AI-generated engagement comment
    """
    summary: str = Field(..., description="Concise summary of the post")
    sentiment: Sentiment = Field(..., description="Detected sentiment")
    topics: List[str] = Field(..., description="Main topics discussed in the post")
    suggested_comment: str = Field(..., description="AI-generated comment suggestion")
    
    class Config:
        schema_extra = {
            "example": {
                "summary": "The post discusses AI's growing role in mobile development...",
                "sentiment": "Positive",
                "topics": ["AI", "Mobile Apps", "Swift"],
                "suggested_comment": "Great insight! I've noticed similar trends in mobile AI apps recently."
            }
        }
