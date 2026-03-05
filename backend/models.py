from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import relationship

from database import Base

class LearnerProfile(Base):
    __tablename__ = "learner_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    level_of_education = Column(String) # "highschool" or "college"
    school_name = Column(String)
    
    # Store settings as JSON strings to maintain flexibility
    learning_style_preferences = Column(JSON, default={})
    pace_and_depth = Column(JSON, default={})
    accessibility_needs = Column(JSON, default={})
    study_habits_and_goals = Column(JSON, default={})
    study_session_duration_pref = Column(JSON, default={})
    
    sessions = relationship("StudySession", back_populates="learner")

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learner_profiles.id"))
    course_name = Column(String)
    topic = Column(String)
    session_duration_minutes = Column(Integer)
    
    learner = relationship("LearnerProfile", back_populates="sessions")
    materials = relationship("CourseContent", back_populates="session")
    messages = relationship("Message", back_populates="session")

class CourseContent(Base):
    """Represents an uploaded file/material associated with a session."""
    __tablename__ = "course_contents"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id"))
    filename = Column(String)
    content_type = Column(String) # "pdf", "image", "audio", "video"
    raw_text = Column(Text)
    
    session = relationship("StudySession", back_populates="materials")

class Message(Base):
    """Represents a chat message within a study session."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id"))
    role = Column(String) # "user", "assistant", "system"
    content = Column(Text)
    
    session = relationship("StudySession", back_populates="messages")
