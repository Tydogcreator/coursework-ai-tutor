from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coursework Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Coursework Analyzer API"}

@app.post("/profiles/", response_model=schemas.LearnerProfile)
def create_profile(profile: schemas.LearnerProfileCreate, db: Session = Depends(get_db)):
    db_profile = models.LearnerProfile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@app.get("/profiles/{profile_id}", response_model=schemas.LearnerProfile)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = db.query(models.LearnerProfile).filter(models.LearnerProfile.id == profile_id).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@app.post("/sessions/", response_model=schemas.StudySession)
def create_session(session: schemas.StudySessionCreate, db: Session = Depends(get_db)):
    db_session = models.StudySession(**session.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@app.get("/sessions/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):
    db_session = db.query(models.StudySession).filter(models.StudySession.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.query(models.Message).filter(models.Message.session_id == session_id).all()
    
    return {
        "session": db_session,
        "history": [{"role": m.role, "content": m.content} for m in messages]
    }

from llm_service import generate_chat_response
from ingestion_service import process_upload
import os

@app.post("/upload/")
async def upload_file(session_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_session = db.query(models.StudySession).filter(models.StudySession.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    contents = await file.read()
    
    # Save file temporarily if it's audio for Whisper to read from disk
    file_path = None
    if file.filename.lower().endswith(('.mp3', '.wav', '.m4a')):
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(contents)
            
    extracted_text = process_upload(file.filename, contents, file_path)
    
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    # Save to db
    db_content = models.CourseContent(
        session_id=session_id,
        filename=file.filename,
        content_type=file.content_type,
        raw_text=extracted_text
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    
    return {"message": "File processed", "content_id": db_content.id}

@app.post("/chat/", response_model=schemas.MessageBase)
def chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    db_session = db.query(models.StudySession).filter(models.StudySession.id == request.session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Load Learner Profile
    learner_profile_dict = {}
    if db_session.learner:
        learner_profile_dict = {
            "name": db_session.learner.name,
            "level_of_education": db_session.learner.level_of_education,
            "school_name": db_session.learner.school_name,
            "learning_style_preferences": db_session.learner.learning_style_preferences,
            "pace_and_depth": db_session.learner.pace_and_depth,
            "accessibility_needs": db_session.learner.accessibility_needs,
            "study_habits_and_goals": db_session.learner.study_habits_and_goals,
            "study_session_duration_pref": db_session.learner.study_session_duration_pref
        }

    # Save User Message
    user_msg = models.Message(session_id=request.session_id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # Load recent context
    messages = db.query(models.Message).filter(models.Message.session_id == request.session_id).order_by(models.Message.id.asc()).all()
    formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages]

    # Load extracted text from materials if this is the start of the session (or inject generally)
    materials = db.query(models.CourseContent).filter(models.CourseContent.session_id == request.session_id).all()
    
    # We optionally inject the document text into the user's prompt covertly if there are materials
    if materials and len(messages) == 1:
        doc_context = "\n\n--- UPLOADED COURSE MATERIALS ---\n"
        for mat in materials:
            doc_context += f"Filename: {mat.filename}\nContent:\n{mat.raw_text}\n\n"
        doc_context += "---------------------------------\n"
        formatted_messages[-1]["content"] += doc_context

    # Call LLM
    response_text = generate_chat_response(formatted_messages, learner_profile_dict)

    # Save Assistant Message
    assistant_msg = models.Message(session_id=request.session_id, role="assistant", content=response_text)
    db.add(assistant_msg)
    db.commit()

    return {"role": "assistant", "content": response_text}
