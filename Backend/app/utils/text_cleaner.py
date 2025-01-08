"""
text_cleaner.py

Utility functions to clean and prepare text for AI processing
"""

import re
from typing import  Optional

def clean_text(text: str) -> str:
    """
    Grab post content and clean up extra noise before sending to AI
    This keeps the summarization accurate and context-aware
    
    Args:
        text: Raw text from social media post
        
    Returns:
        Cleaned text ready for AI processing
    """
    if not text:
        return ""
    
    # Remove URLs (they don't add much context for AI)
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Strip out HTML tags if any snuck through
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove excessive whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Get rid of leading/trailing spaces
    text = text.strip()
    
    return text

def extract_hashtags(text: str) -> list[str]:
    """
    Pull out hashtags from the text
    These can be useful for topic detection
    
    Args:
        text: Text potentially containing hashtags
        
    Returns:
        List of hashtags without the # symbol
    """
    hashtags = re.findall(r'#(\w+)', text)
    return hashtags

def truncate_text(text: str, max_length: int = 5000) -> str:
    """
    Cut down really long posts to avoid token limits
    
    Args:
        text: Original text
        max_length: Maximum character count
        
    Returns:
        Truncated text if needed
    """
    if len(text) <= max_length:
        return text
    
    # Try to cut at a sentence boundary if possible
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    
    if last_period > max_length * 0.8:  # Only if we're not losing too much
        return truncated[:last_period + 1]
    
    return truncated + "..."

def is_valid_content(text: str) -> bool:
    """
    Quick check to make sure we actually have usable content
    
    Args:
        text: Text to validate
        
    Returns:
        True if text is substantial enough to analyze
    """
    if not text or len(text.strip()) < 10:
        return False
    
    # Make sure it's not just special characters or whitespace
    alphanumeric_count = sum(c.isalnum() for c in text)
    return alphanumeric_count > 5
