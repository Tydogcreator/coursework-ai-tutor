# Coursework AI Tutor

A full-stack, AI-powered tutoring platform designed to ingest multimodal course materials (PDFs, Images, Audio) and generate highly personalized, state-aware study guides. Built with cognitive science principles in mind, the tutor uses strict Socratic-method prompting to ensure **academic integrity** is maintained—it teaches the material instead of just giving away the answers.

![Coursework Analyzer](https://img.shields.io/badge/Status-Active-success) ![License](https://img.shields.io/badge/License-MIT-blue)

---

## ✨ Key Features
- **Multimodal Ingestion**: Upload lecture slides (PDFs), handwritten notes (Images/OCR), and recorded lectures (Audio/Video).
- **Stateful Learner Profiles**: The system remembers your education level, learning style, and study preferences across sessions.
- **Strict Guardrails**: Designed to prevent cheating. It acts as a true tutor by utilizing the Socratic method to guide students to answers.
- **Local/Cloud LLM Support**: Works seamlessly with OpenAI API, generic OpenAI-compatible endpoints (like Groq), or completely locally and privately using **Ollama**.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your machine:

1. **Node.js** (v18 or higher) - For the React frontend.
2. **Python** (v3.9 or higher) - For the FastAPI backend.
3. **Tesseract OCR** (Optional but highly recommended) - Required for reading text from images/handwritten notes. [Download here](https://github.com/UB-Mannheim/tesseract/wiki).
4. **ffmpeg** (Optional but highly recommended) - Required for OpenAI Whisper to process audio/video files. [Download here](https://ffmpeg.org/download.html).

---

## 🚀 Quick Start & Installation

Follow these steps to get the application running locally on your machine.

### Step 1: Clone the Repository
```bash
git clone https://github.com/Tydogcreator/coursework-ai-tutor.git
cd coursework-ai-tutor
```

### Step 2: Set Up the Backend
The backend is built with Python and FastAPI. It uses SQLite for lightweight, zero-configuration local storage.

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   - **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your Environment Variables:
   Create a new file named `.env` inside the `backend` folder and add your API credentials:
   ```env
   # Ensure you put in a valid OpenAI API key or use a local one (see Local Models section below)
   OPENAI_API_KEY=your_openai_key
   MODEL_NAME=gpt-4o
   ```

### Step 3: Set Up the Frontend
The frontend is built with React, Vite, and Tailwind CSS.

1. Open a **new terminal tab/window** and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node modules:
   ```bash
   npm install
   ```

---

## 🏃‍♂️ Running the Application

To use the Coursework AI Tutor, you need to run both the backend and frontend servers simultaneously. 

**Terminal 1 (Backend):**
```bash
cd backend
# Make sure your virtual environment is activated!
uvicorn main:app --reload
```
*The API will start running at: `http://localhost:8000`*

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
*The web interface will start running at: `http://localhost:5173`*

**Open your browser and navigate to `http://localhost:5173` to start studying!**

---

## 🧠 Universal Model Support (Local Models, Groq, etc.)

This project uses the official **OpenAI SDK** under the hood. Because almost all modern AI providers use the OpenAI standard format, you can swap the AI model you use by simply changing two environment variables in your `backend/.env` file. No code changes required!

### 1. Using Local Models via Ollama (100% Free & Private)
If you prefer to run models locally on your computer offline (like Qwen, Llama 3, or Phi):

1. Download and install [Ollama](https://ollama.com/).
2. Pull your model of choice (e.g., Llama 3):
   ```bash
   ollama run llama3
   ```
3. Update your `backend/.env`:
   ```env
   OPENAI_API_KEY=ollama
   MODEL_NAME=llama3
   OPENAI_BASE_URL=http://localhost:11434/v1
   ```

### 2. Using Generic OpenAI-Compatible Endpoints (Groq, LM Studio, etc.)
If you use LM Studio or Groq for ultra-fast generation:
```env
OPENAI_API_KEY=your_groq_or_custom_key
MODEL_NAME=llama-3.1-70b-versatile
OPENAI_BASE_URL=https://api.groq.com/openai/v1 # Or your custom endpoint url
```

---

## 🏗️ Architecture Stack
- **Frontend Core:** React, Vite, Tailwind CSS v4
- **Markdown Rendering:** `react-markdown`
- **Backend Core:** Python, FastAPI, SQLAlchemy (SQLite)
- **Data Ingestion:** `pdfplumber` (PDF), `pytesseract` (Images), `openai-whisper` (Audio)
- **LLM Context Injection:** Custom Pydantic models for tracking session history and dynamic learner profiles.
