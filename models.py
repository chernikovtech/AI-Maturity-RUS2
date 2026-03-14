"""
Database models
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, Float, DateTime, Integer, ForeignKey, Text, Date, JSON
from sqlalchemy.orm import relationship
from database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    event_date = Column(Date, nullable=True)
    status = Column(String(20), default="active")  # active / closed
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    participants = relationship("Participant", back_populates="event", lazy="dynamic")


class Participant(Base):
    __tablename__ = "participants"

    id = Column(String, primary_key=True, default=gen_uuid)
    event_id = Column(String, ForeignKey("events.id"), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    country = Column(String(100), nullable=True)
    industry = Column(String(255), nullable=True)
    consent_store = Column(Boolean, default=False)
    submitted_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)  # soft delete
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    event = relationship("Event", back_populates="participants")
    responses = relationship("Response", back_populates="participant", cascade="all, delete-orphan")
    score = relationship("Score", back_populates="participant", uselist=False, cascade="all, delete-orphan")


class Response(Base):
    __tablename__ = "responses"

    id = Column(String, primary_key=True, default=gen_uuid)
    participant_id = Column(String, ForeignKey("participants.id"), nullable=False, index=True)
    question_key = Column(String(50), nullable=False)
    answer_value = Column(Integer, nullable=False)  # 1-4
    dimension = Column(String(50), nullable=False)

    participant = relationship("Participant", back_populates="responses")


class Score(Base):
    __tablename__ = "scores"

    id = Column(String, primary_key=True, default=gen_uuid)
    participant_id = Column(String, ForeignKey("participants.id"), nullable=False, unique=True, index=True)
    total_score = Column(Float, nullable=False)  # 0-100
    level = Column(String(50), nullable=False)  # Explorer, Learner, Practitioner, Architect
    dimension_scores = Column(JSON, nullable=False)  # {"context_assembly": 66.7, ...}
    computed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    participant = relationship("Participant", back_populates="score")
