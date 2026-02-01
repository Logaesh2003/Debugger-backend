# Debugger Backend

AI-powered code debugging and fixing service that uses LLM to analyze and fix error code from the VSCode Debugger Extension.

## Features

- 🤖 **AI-Powered Fixes** - Uses Groq inference with openAI models to analyze and fix code
- ⚡ **Fast Response** - Groq provides ultra-fast inference times
- 🔧 **Simple API** - Single endpoint that accepts code and returns fixes

## Setup

### 1. Clone & Install Dependencies

```bash
cd Debugger-backend
pip install -r requirements.txt
```

### 2. Configure API Key

Get a free API key from [Groq Console](https://console.groq.com/keys) and add it to `.env`:

```env
GROQ_API_KEY=gsk_your_api_key_here
```

### 3. Run the Server

```bash
python main.py
```

Server runs at `http://localhost:8000`

## API

### POST `/fix`

Analyzes code and returns a fix with explanation.

**Request:**
```json
{
    "code": "const x = 5"
}
```

**Response:**
```json
{
    "explanation": "It looks like you have a syntax error. I added a missing semicolon.",
    "fix": "const x = 5;"
}
```

### GET `/health`

Health check endpoint.

## Project Structure

```
Debugger-backend/
├── main.py              # FastAPI application
├── agents/
│   └── code_fixer.py    # LLM agent for code fixing
├── config/
│   └── settings.py      # Configuration and environment
├── requirements.txt     # Python dependencies
└── .env                 # API keys (not committed)
```

## Configuration

Optional environment variables in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | - | Your Groq API key (required) |
| `MODEL_NAME` | `llama-3.3-70b-versatile` | LLM model to use |
| `TEMPERATURE` | `0.3` | Response creativity (0-1) |
| `MAX_TOKENS` | `2048` | Maximum response length |
