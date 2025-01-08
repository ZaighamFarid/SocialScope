"""
summarizer_service.py

Uses OpenAI to generate summaries, detect sentiment, and extract topics
"""

import os
from typing import Dict, List
from openai import OpenAI
from app.models.response_model import Sentiment

class SummarizerService:
    """Handles AI-powered text analysis using OpenAI"""
    
    def __init__(self):
        # Grab API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Fast and cost-effective for this use case
    
    def analyze_content(self, text: str) -> Dict:
        """
        Send text to AI for comprehensive analysis
        Returns summary, sentiment, and key topics all in one go
        
        Args:
            text: Cleaned post content
            
        Returns:
            Dictionary with summary, sentiment, and topics
        """
        prompt = self._build_analysis_prompt(text)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing social media content. Provide concise, accurate analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse AI response
            result_text = response.choices[0].message.content
            return self._parse_analysis_response(result_text)
            
        except Exception as e:
            raise ValueError(f"AI analysis failed: {str(e)}")
    
    def _build_analysis_prompt(self, text: str) -> str:
        """
        Craft a clear prompt for the AI to get consistent results
        We want summary, sentiment, and topics in a structured format
        """
        return f"""Analyze this social media post and provide:

1. A concise summary (2-3 sentences max)
2. Overall sentiment (choose ONLY: Positive, Neutral, or Negative)
3. 3-5 key topics or themes

Post content:
\"\"\"{text}\"\"\"

Format your response EXACTLY like this:
SUMMARY: [your summary here]
SENTIMENT: [Positive/Neutral/Negative]
TOPICS: [topic1, topic2, topic3]
"""
    
    def _parse_analysis_response(self, response_text: str) -> Dict:
        """
        Extract structured data from AI's text response
        Parse out summary, sentiment, and topics into usable format
        """
        lines = response_text.strip().split('\n')
        
        summary = ""
        sentiment = Sentiment.NEUTRAL
        topics = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("SUMMARY:"):
                summary = line.replace("SUMMARY:", "").strip()
            
            elif line.startswith("SENTIMENT:"):
                sentiment_text = line.replace("SENTIMENT:", "").strip()
                # Map to our enum
                if "positive" in sentiment_text.lower():
                    sentiment = Sentiment.POSITIVE
                elif "negative" in sentiment_text.lower():
                    sentiment = Sentiment.NEGATIVE
                else:
                    sentiment = Sentiment.NEUTRAL
            
            elif line.startswith("TOPICS:"):
                topics_text = line.replace("TOPICS:", "").strip()
                # Split by commas and clean up
                topics = [t.strip() for t in topics_text.split(',')]
                # Remove any empty strings
                topics = [t for t in topics if t]
        
        return {
            "summary": summary or "No summary available",
            "sentiment": sentiment,
            "topics": topics or ["General"]
        }
