# 📚 Coursework AI Tutor

**Your free, private AI study buddy.** Upload your lecture slides, notes, or recordings and get personalized study guides, practice quizzes, and Socratic tutoring — all running on your own computer. No accounts, no subscriptions, no data leaving your machine.

![Status](https://img.shields.io/badge/Status-Active-success) ![License](https://img.shields.io/badge/License-MIT-blue) ![Cost](https://img.shields.io/badge/Cost-100%25%20Free-brightgreen)

---

## ⚡ 60-Second Setup (Free, No API Key Needed)

You only need to install **3 things** and then copy-paste a few commands. That's it.

### What You Need to Install First

| # | What | Why | Download Link |
|---|------|-----|---------------|
| 1 | **Ollama** | This is the free AI brain that runs on your computer | [ollama.com](https://ollama.com/) |
| 2 | **Python** (3.10+) | Runs the backend server | [python.org](https://www.python.org/downloads/) |
| 3 | **Node.js** (18+) | Runs the web interface | [nodejs.org](https://nodejs.org/) |

> **💡 Tip:** When installing Python, make sure to check the box that says **"Add Python to PATH"**. This is important!

---

### Step 1: Download an AI Model (One Time Only)

After installing Ollama, open your terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
ollama run llama3
```

This downloads a free AI model to your computer (~4GB). It only needs to happen once. When you see it respond to you, you're good — type `/bye` to exit.

### Step 2: Download This Project

```bash
git clone https://github.com/Tydogcreator/coursework-ai-tutor.git
cd coursework-ai-tutor
```

> **Don't have git?** You can also click the green **"Code"** button on GitHub and select **"Download ZIP"**, then unzip the folder.

### Step 3: Set Up the Backend (One Time Only)

Open a terminal inside the project folder and run:

**Windows:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Create Your Settings File (One Time Only)

Create a new file called `.env` inside the `backend` folder and paste this in:

```env
OPENAI_API_KEY=ollama
MODEL_NAME=llama3
OPENAI_BASE_URL=http://localhost:11434/v1
```

That's it. No API keys, no sign-ups, no credit cards.

### Step 5: Set Up the Frontend (One Time Only)

Open a **second** terminal window and run:

```bash
cd frontend
npm install
```

---

## 🟢 How to Start Studying (Every Time You Want to Use It)

You need to have **two terminal windows** open. Think of it like starting two apps.

**Terminal 1 — Start the AI Engine:**
```bash
cd backend
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux
uvicorn main:app --reload
```

**Terminal 2 — Start the Web Interface:**
```bash
cd frontend
npm run dev
```

**Now open your browser and go to: [http://localhost:5173](http://localhost:5173)**

🎉 **You're in!** Create your learner profile, upload your study materials, and start asking questions.

---

## 📖 How to Use the Tutor

1. **Create Your Profile** — Enter your name, education level, and school. This helps the tutor personalize explanations to your level.
2. **Upload Your Materials** — Click the upload button (📎) to upload lecture slides (PDF), photos of handwritten notes, or audio recordings of lectures.
3. **Ask Questions** — Type anything in the chat box:
   - *"Explain Chapter 3 like I'm 5"*
   - *"Create a practice quiz on this material"*
   - *"What are the key concepts I should know for the exam?"*
   - *"Make me a study guide"*
4. **The tutor will NOT give you direct answers to homework.** It's designed to teach you by asking guiding questions (the Socratic method), so you actually learn the material.

---

## 💰 Want to Use a Different AI Model?

The default setup uses **Ollama** (completely free, runs on your computer). But if you want to use a cloud-based model instead, just change the 3 lines in your `backend/.env` file:

### Option A: Use OpenAI (GPT-4o) — Paid
```env
OPENAI_API_KEY=sk-your-key-here
MODEL_NAME=gpt-4o
# Delete or comment out the OPENAI_BASE_URL line
```
Get your API key at [platform.openai.com](https://platform.openai.com/api-keys).

### Option B: Use Groq (Llama 3.1 70B) — Free Tier Available
```env
OPENAI_API_KEY=gsk_your-groq-key
MODEL_NAME=llama-3.1-70b-versatile
OPENAI_BASE_URL=https://api.groq.com/openai/v1
```
Get a free API key at [console.groq.com](https://console.groq.com).

### Option C: Use a Different Ollama Model
```bash
ollama run qwen2.5    # or mistral, phi3, gemma2, etc.
```
Then update your `.env`:
```env
OPENAI_API_KEY=ollama
MODEL_NAME=qwen2.5
OPENAI_BASE_URL=http://localhost:11434/v1
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Cannot connect to server"** | Make sure both terminals are running (backend AND frontend) |
| **"Error connecting to LLM"** | Make sure Ollama is running. Open a terminal and type `ollama serve` |
| **Page is blank** | Hard refresh your browser (Ctrl+Shift+R) |
| **Pip install fails** | Make sure Python is at version 3.10 or higher: `python --version` |

---

## 🏗️ Tech Stack (For Developers)
- **Frontend:** React, Vite, Tailwind CSS v4, react-markdown, Lucide icons
- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **AI Integration:** OpenAI SDK (compatible with Ollama, Groq, and any OpenAI-format endpoint)
- **Data Ingestion:** pdfplumber (PDFs), pytesseract (Image OCR), openai-whisper (Audio transcription)
