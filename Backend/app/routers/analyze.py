"""
analyze.py

Main API endpoint for post analysis
"""

from fastapi import APIRouter, HTTPException
from app.models.request_model import AnalyzeRequest
from app.models.response_model import AnalyzeResponse
from app.services.scraper_service import ScraperService
from app.services.summarizer_service import SummarizerService
from app.services.comment_service import CommentService

router = APIRouter()

# Initialize services (could also use dependency injection here)
scraper = ScraperService()
summarizer = SummarizerService()
commenter = CommentService()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_post(request: AnalyzeRequest):
    """
    Analyze a social media post and generate engagement suggestions
    
    Takes a post URL, fetches content, analyzes it with AI, and returns:
    - Summary of the post
    - Sentiment analysis
    - Key topics
    - Suggested comment in the requested tone
    """
    
    try:
        # Step 1: Grab the post content from the URL
        post_data = scraper.fetch_post_content(request.url)
        post_text = post_data["text"]
        
        # Step 2: Analyze the content with AI
        analysis = summarizer.analyze_content(post_text)
        
        # Step 3: Generate a natural comment based on analysis
        comment = commenter.generate_comment(
            summary=analysis["summary"],
            sentiment=analysis["sentiment"].value,
            topics=analysis["topics"],
            tone=request.tone
        )
        
        # Package everything up for the response
        return AnalyzeResponse(
            summary=analysis["summary"],
            sentiment=analysis["sentiment"],
            topics=analysis["topics"],
            suggested_comment=comment
        )
        
    except ValueError as e:
        # These are expected errors (invalid URL, fetch failures, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
