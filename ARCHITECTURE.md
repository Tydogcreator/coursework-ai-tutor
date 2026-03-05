# Architecture Overview

This document describes the system architecture, design decisions, and data flow of the Coursework AI Tutor.

## System Design

```
┌─────────────────────────┐     HTTP/JSON      ┌──────────────────────────────┐
│                         │ ◄────────────────► │                              │
│   React Frontend        │                    │   FastAPI Backend             │
│   (Vite + Tailwind)     │                    │                              │
│                         │                    │  ┌─────────────────────┐     │
│  ┌───────────────────┐  │                    │  │  Learner Profile    │     │
│  │ LearnerProfile    │  │  POST /profiles/   │  │  Manager            │     │
│  │ Component         │──┼───────────────────►│  └─────────┬───────────┘     │
│  └───────────────────┘  │                    │            │                  │
│                         │                    │  ┌─────────▼───────────┐     │
│  ┌───────────────────┐  │  POST /chat/       │  │  Context Injector   │     │
│  │ ChatInterface     │──┼───────────────────►│  │  (System Prompt +   │     │
│  │ Component         │  │                    │  │   Profile + History) │     │
│  └───────────────────┘  │                    │  └─────────┬───────────┘     │
│                         │                    │            │                  │
│  ┌───────────────────┐  │  POST /upload/     │  ┌─────────▼───────────┐     │
│  │ File Upload       │──┼───────────────────►│  │  Multimodal         │     │
│  │ Handler           │  │                    │  │  Ingestion Pipeline  │     │
│  └───────────────────┘  │                    │  │  (PDF/OCR/Audio)    │     │
│                         │                    │  └─────────┬───────────┘     │
└─────────────────────────┘                    │            │                  │
                                               │  ┌─────────▼───────────┐     │
                                               │  │  LLM Service        │────►│ Ollama / OpenAI / Groq
                                               │  │  (OpenAI SDK)       │     │
                                               │  └─────────────────────┘     │
                                               │            │                  │
                                               │  ┌─────────▼───────────┐     │
                                               │  │  SQLite Database    │     │
                                               │  │  (SQLAlchemy ORM)   │     │
                                               │  └─────────────────────┘     │
                                               └──────────────────────────────┘
```

## Key Design Decisions

### 1. Stateless LLM, Stateful Application
The LLM itself is stateless — it has no memory between calls. The application layer is responsible for:
- Persisting the **Learner Profile** (education level, learning style, accessibility needs)
- Storing **chat history** per session in SQLite
- Injecting all of this context into the system prompt on every LLM call

This means the user's experience feels persistent and personalized, even though the underlying model treats every request as brand new.

### 2. Universal Model Compatibility via OpenAI SDK
Rather than hard-coding a specific AI provider, the backend uses the official **OpenAI Python SDK** with a configurable `base_url`. This is possible because virtually all modern LLM providers (Ollama, Groq, LM Studio, etc.) have adopted the OpenAI chat completions format as an industry standard. Swapping models requires changing only environment variables — zero code changes.

### 3. Multimodal Ingestion as a Pipeline
Uploaded files are routed through a pipeline based on file extension:

| File Type | Library | Output |
|-----------|---------|--------|
| `.pdf` | pdfplumber | Extracted text |
| `.png`, `.jpg` | pytesseract (Tesseract OCR) | OCR text |
| `.mp3`, `.wav` | openai-whisper | Transcribed text |
| `.txt`, `.md` | Built-in | Raw text |

All outputs are normalized to plain text and stored in the database, then injected into the LLM context when the user asks a question.

### 4. Socratic Method Enforcement
The system prompt (stored privately in `docs/system_prompt.md`) enforces strict academic integrity rules:
- **Never** completes graded assignments or writes essays
- **Always** uses guiding questions instead of direct answers
- **Transparent failure** — the tutor explicitly says when it doesn't know something
- These guardrails are baked into the system prompt, not the application code, making them model-agnostic

### 5. Progressive Onboarding
The Learner Profile is designed to be built gradually through conversation, not through a long questionnaire upfront. The initial form captures only the essentials (name, education level, school). Advanced preferences (learning style, pace, accessibility needs) are stored as flexible JSON fields that can be updated over time.

## Database Schema

```
learner_profiles
├── id (PK)
├── name
├── level_of_education
├── school_name
├── learning_style_preferences (JSON)
├── pace_and_depth (JSON)
├── accessibility_needs (JSON)
├── study_habits_and_goals (JSON)
└── study_session_duration_pref (JSON)

study_sessions
├── id (PK)
├── learner_id (FK → learner_profiles)
├── course_name
├── topic
└── session_duration_minutes

course_contents
├── id (PK)
├── session_id (FK → study_sessions)
├── filename
├── content_type
└── raw_text

messages
├── id (PK)
├── session_id (FK → study_sessions)
├── role ("user" | "assistant" | "system")
└── content
```

## Data Flow: Chat Request

1. User types a message in the React frontend
2. Frontend sends `POST /chat/` with `{session_id, message}`
3. Backend loads the **Learner Profile** from the database
4. Backend saves the user message to the `messages` table
5. Backend loads all previous messages for this session
6. If course materials exist and this is the first message, their extracted text is appended to the user's message
7. The **system prompt** + **learner profile JSON** + **message history** are assembled into a single prompt
8. The assembled prompt is sent to the LLM via the OpenAI SDK
9. The LLM response is saved to the `messages` table
10. The response is returned to the frontend and rendered as Markdown

## Project Structure

```
coursework-ai-tutor/
├── README.md                  # User-facing setup guide
├── ARCHITECTURE.md            # This file
├── backend/
│   ├── main.py                # FastAPI app, all API endpoints
│   ├── models.py              # SQLAlchemy ORM models
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── database.py            # SQLite connection setup
│   ├── llm_service.py         # LLM integration (OpenAI SDK)
│   ├── ingestion_service.py   # Multimodal file processing
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment config (not tracked)
├── frontend/
│   ├── src/
│   │   ├── main.tsx           # React entry point
│   │   ├── App.jsx            # App router (Profile → Chat)
│   │   ├── index.css          # Tailwind v4 theme
│   │   └── components/
│   │       ├── LearnerProfile.jsx   # Onboarding form
│   │       └── ChatInterface.jsx    # Chat UI with Markdown
│   ├── package.json
│   └── vite.config.ts
└── docs/
    └── system_prompt.md       # Prompt v7 (not tracked in git)
```
