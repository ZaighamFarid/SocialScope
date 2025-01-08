"""
test_analyze_endpoint.py

Tests for the /analyze endpoint
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app
from app.models.response_model import Sentiment

client = TestClient(app)

@pytest.fixture
def mock_scraper():
    """Mock scraper service to avoid real network calls"""
    with patch('app.routers.analyze.scraper') as mock:
        mock.fetch_post_content.return_value = {
            "text": "This is a test post about AI and mobile development.",
            "platform": "twitter"
        }
        yield mock

@pytest.fixture
def mock_summarizer():
    """Mock AI summarizer to avoid real API calls"""
    with patch('app.routers.analyze.summarizer') as mock:
        mock.analyze_content.return_value = {
            "summary": "A test post discussing AI in mobile development.",
            "sentiment": Sentiment.POSITIVE,
            "topics": ["AI", "Mobile", "Development"]
        }
        yield mock

@pytest.fixture
def mock_commenter():
    """Mock comment generator"""
    with patch('app.routers.analyze.commenter') as mock:
        mock.generate_comment.return_value = "Great insights on AI!"
        yield mock

def test_health_check():
    """Make sure the API is up and running"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_endpoint_success(mock_scraper, mock_summarizer, mock_commenter):
    """Test successful post analysis"""
    payload = {
        "url": "https://twitter.com/test/status/123",
        "tone": "friendly"
    }
    
    response = client.post("/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check all expected fields are present
    assert "summary" in data
    assert "sentiment" in data
    assert "topics" in data
    assert "suggested_comment" in data
    
    # Verify the mocked values came through
    assert data["sentiment"] == "Positive"
    assert len(data["topics"]) == 3
    assert data["suggested_comment"] == "Great insights on AI!"

def test_analyze_endpoint_invalid_url(mock_scraper, mock_summarizer, mock_commenter):
    """Test error handling for invalid URLs"""
    mock_scraper.fetch_post_content.side_effect = ValueError("Invalid URL")
    
    payload = {
        "url": "not-a-valid-url",
        "tone": "friendly"
    }
    
    response = client.post("/analyze", json=payload)
    assert response.status_code == 400

def test_analyze_endpoint_missing_url():
    """Test validation for missing required fields"""
    payload = {
        "tone": "friendly"
    }
    
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422  # Validation error

def test_different_tones(mock_scraper, mock_summarizer, mock_commenter):
    """Test that different tones are properly passed through"""
    tones = ["professional", "friendly", "funny", "supportive"]
    
    for tone in tones:
        payload = {
            "url": "https://twitter.com/test/status/123",
            "tone": tone
        }
        
        response = client.post("/analyze", json=payload)
        assert response.status_code == 200
        
        # Verify tone was passed to comment service
        mock_commenter.generate_comment.assert_called()
