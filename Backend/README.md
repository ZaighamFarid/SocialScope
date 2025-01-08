# Social Scope Backend

FastAPI backend for Social Scope - AI-powered social media post analysis.

## Quick Start

### 1. Set up environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
```

### 3. Run

```bash
# Using the run script
./run.sh

# Or manually
uvicorn app.main:app --reload
```

Server runs at: `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

## Testing

```bash
# Run all tests
pytest app/tests/ -v

# With coverage
pytest app/tests/ -v --cov=app

# Specific test file
pytest app/tests/test_analyze_endpoint.py -v
```

## API Endpoints

### `POST /analyze`
Analyze a social media post.

**Request:**
```json
{
  "url": "https://twitter.com/user/status/12345",
  "tone": "friendly"
}
```

**Response:**
```json
{
  "summary": "Post summary...",
  "sentiment": "Positive",
  "topics": ["AI", "Tech"],
  "suggested_comment": "Great insights!"
}
```

### `GET /health`
Health check endpoint.

## Project Structure

```
app/
├── main.py           # FastAPI app entry point
├── routers/          # API endpoints
├── services/         # Business logic
├── models/           # Pydantic models
├── utils/            # Utility functions
└── tests/            # Test suite
```

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
