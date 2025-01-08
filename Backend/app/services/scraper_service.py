"""
scraper_service.py

Handles fetching content from various social media platforms
"""

import re
from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup
from app.utils.text_cleaner import clean_text, is_valid_content

class ScraperService:
    """Service to extract content from social media URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        # Set a realistic user agent so sites don't block us
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def fetch_post_content(self, url: str) -> Dict[str, str]:
        """
        Grab post content from URL and clean up extra noise
        Auto-detect platform and use the right extraction method
        
        Args:
            url: Social media post URL
            
        Returns:
            Dictionary with 'text' and 'platform' keys
            
        Raises:
            ValueError: If URL is invalid or content can't be fetched
        """
        platform = self._detect_platform(url)
        
        try:
            if platform == "twitter":
                content = self._fetch_twitter_content(url)
            elif platform == "reddit":
                content = self._fetch_reddit_content(url)
            elif platform == "medium":
                content = self._fetch_medium_content(url)
            else:
                # Generic fallback for other sites
                content = self._fetch_generic_content(url)
            
            # Make sure we actually got something usable
            if not is_valid_content(content):
                raise ValueError("Couldn't extract meaningful content from that URL")
            
            return {
                "text": clean_text(content),
                "platform": platform
            }
            
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch content from URL: {str(e)}")
    
    def _detect_platform(self, url: str) -> str:
        """Figure out which platform this URL is from"""
        url_lower = url.lower()
        
        if "twitter.com" in url_lower or "x.com" in url_lower:
            return "twitter"
        elif "reddit.com" in url_lower:
            return "reddit"
        elif "medium.com" in url_lower:
            return "medium"
        else:
            return "generic"
    
    def _fetch_twitter_content(self, url: str) -> str:
        """
        Extract tweet text
        Note: Twitter's API access is limited, so we do basic scraping here
        For production, consider using official API with proper auth
        """
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try different selectors that Twitter uses
        tweet_text = None
        
        # Look for meta tags first (most reliable)
        meta_desc = soup.find('meta', {'property': 'og:description'})
        if meta_desc:
            tweet_text = meta_desc.get('content')
        
        # Fallback to other common patterns
        if not tweet_text:
            # Try finding tweet text in common div classes
            tweet_div = soup.find('div', {'data-testid': 'tweetText'})
            if tweet_div:
                tweet_text = tweet_div.get_text()
        
        return tweet_text or "Unable to extract tweet content"
    
    def _fetch_reddit_content(self, url: str) -> str:
        """Pull content from Reddit post"""
        # Add .json to Reddit URL for easy parsing
        if not url.endswith('.json'):
            json_url = url.rstrip('/') + '.json'
        else:
            json_url = url
        
        response = self.session.get(json_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Reddit's JSON structure has post data in first element
        if data and len(data) > 0:
            post_data = data[0]['data']['children'][0]['data']
            
            # Combine title and selftext for full context
            title = post_data.get('title', '')
            body = post_data.get('selftext', '')
            
            return f"{title}\n\n{body}" if body else title
        
        return "Unable to extract Reddit post content"
    
    def _fetch_medium_content(self, url: str) -> str:
        """Extract article content from Medium"""
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Medium uses article tags for content
        article = soup.find('article')
        if article:
            # Get all paragraphs and join them
            paragraphs = article.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs])
            return content
        
        return "Unable to extract Medium article content"
    
    def _fetch_generic_content(self, url: str) -> str:
        """
        Generic fallback for other sites
        Tries to extract main content using common patterns
        """
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try meta description first
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc.get('content')
        
        # Look for article or main content areas
        for tag in ['article', 'main', 'div[role="main"]']:
            content_area = soup.find(tag)
            if content_area:
                text = content_area.get_text(separator=' ', strip=True)
                if len(text) > 50:  # Make sure it's substantial
                    return text
        
        # Last resort: get all paragraph text
        paragraphs = soup.find_all('p')
        if paragraphs:
            text = ' '.join([p.get_text() for p in paragraphs])
            return text
        
        return "Unable to extract content from this URL"
