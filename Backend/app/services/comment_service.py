"""
comment_service.py

Generates natural, engaging comments based on post content and desired tone
"""

import os
from openai import OpenAI
from app.models.request_model import CommentTone

class CommentService:
    """Handles AI-powered comment generation"""
    
    def __init__(self):
        # Grab API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def generate_comment(self, summary: str, sentiment: str, topics: list, tone: CommentTone) -> str:
        """
        Create a natural, human-sounding comment based on post analysis
        The comment should feel authentic and match the requested tone
        
        Args:
            summary: Post summary for context
            sentiment: Detected sentiment of the post
            topics: Key topics from the post
            tone: Desired tone for the comment
            
        Returns:
            Generated comment text
        """
        prompt = self._build_comment_prompt(summary, sentiment, topics, tone)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(tone)
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,  # Higher temp for more creative, varied responses
                max_tokens=150
            )
            
            comment = response.choices[0].message.content.strip()
            
            # Remove quotes if AI wrapped the comment in them
            if comment.startswith('"') and comment.endswith('"'):
                comment = comment[1:-1]
            
            return comment
            
        except Exception as e:
            raise ValueError(f"Comment generation failed: {str(e)}")
    
    def _get_system_prompt(self, tone: CommentTone) -> str:
        """
        Set the AI's personality based on desired tone
        This helps ensure consistent voice across comments
        """
        if tone == CommentTone.PROFESSIONAL:
            return "You are a professional industry expert writing thoughtful, respectful comments on social media posts."
        
        elif tone == CommentTone.FRIENDLY:
            return "You are a warm, friendly person writing casual but genuine comments on social media posts."
        
        elif tone == CommentTone.FUNNY:
            return "You are a witty, humorous person writing entertaining comments on social media posts. Keep it light and playful."
        
        elif tone == CommentTone.SUPPORTIVE:
            return "You are an encouraging, empathetic person writing supportive comments on social media posts."
        
        return "You write natural, engaging comments on social media posts."
    
    def _build_comment_prompt(self, summary: str, sentiment: str, topics: list, tone: CommentTone) -> str:
        """
        Build a prompt that gives AI enough context to write a good comment
        Include the post's main points and desired tone
        """
        topics_str = ", ".join(topics[:3])  # Limit to top 3 topics for focus
        
        return f"""Write a brief, natural comment (1-2 sentences max) responding to this social media post:

Summary: {summary}
Sentiment: {sentiment}
Main Topics: {topics_str}

Requirements:
- Write in a {tone.value} tone
- Sound like a real person, not a bot
- Keep it concise (under 30 words)
- Be genuine and add value to the conversation
- Don't use hashtags or emojis unless it fits naturally
- Don't directly repeat phrases from the summary

Write only the comment itself, nothing else."""
