from pydantic import BaseModel
from typing import Optional, Dict

class LearnerProfileBase(BaseModel):
    name: str
    level_of_education: str
    school_name: str
    learning_style_preferences: Optional[Dict] = {}
    pace_and_depth: Optional[Dict] = {}
    accessibility_needs: Optional[Dict] = {}
    study_habits_and_goals: Optional[Dict] = {}
    study_session_duration_pref: Optional[Dict] = {}

class LearnerProfileCreate(LearnerProfileBase):
    pass

class LearnerProfileUpdate(BaseModel):
    learning_style_preferences: Optional[Dict] = None
    pace_and_depth: Optional[Dict] = None
    accessibility_needs: Optional[Dict] = None
    study_habits_and_goals: Optional[Dict] = None
    study_session_duration_pref: Optional[Dict] = None

class LearnerProfile(LearnerProfileBase):
    id: int

    class Config:
        from_attributes = True

class StudySessionBase(BaseModel):
    course_name: str
    topic: str
    session_duration_minutes: int

class StudySessionCreate(StudySessionBase):
    learner_id: int

class StudySession(StudySessionBase):
    id: int
    learner_id: int

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class ChatRequest(BaseModel):
    session_id: int
    message: str
