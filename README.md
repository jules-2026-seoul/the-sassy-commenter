# Sassy Commenter API

A lightweight, sassy LLM response microservice designed to complement the Pink Calculator. Every time a calculation finishes, this service returns a witty, pink-themed reaction using Gemini.

## Prerequisites and API Keys

This service relies on Google's Gemini models to generate sassy responses.

### 1. Obtain a Free API Key
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Sign in and click **Get API key**.
3. Create a new API key in a new or existing Google Cloud project.

### 2. Local Development Setup
To run this locally, configure your API key via environment variables:

#### On Linux/macOS:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

#### Using a `.env` file:
Create a `.env` file in the project root:
```env
GEMINI_API_KEY="your_api_key_here"
```

---

## Running the Server

### Using Python and Uvicorn:
```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Using Docker:
```bash
docker build -t sassy-commenter .
docker run -p 8000:8000 -e GEMINI_API_KEY=$GEMINI_API_KEY sassy-commenter
```
