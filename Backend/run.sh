#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | xargs)
fi

# Run the FastAPI server
uvicorn app.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --reload
