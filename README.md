# Coursework AI Tutor

A full-stack AI tutoring platform that ingests multimodal course materials (PDFs, Images, Audio) to generate highly personalized, state-aware study guides. Features a FastAPI/SQLite backend, a React/Tailwind frontend, local LLM integration, and strict guardrails aligned with cognitive science to enforce the Socratic teaching method.

## Requirements

### Backend
- Python 3.9+
- OpenAI API Key (or local Ollama instance)
- Tesseract OCR (must be installed on your system for image parsing)
- `ffmpeg` (must be installed on your system for Whisper audio parsing)

### Frontend
- Node.js 18+

## Setup Instructions

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_dummy_or_real_key
MODEL_NAME=gpt-4o # Or llama3 if using Ollama
# OLLAMA_BASE_URL=http://localhost:11434/v1 # Uncomment if using Ollama
```

Run the backend server:
```bash
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. API documentation is automatically generated at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.
