"""SQLAlchemy ORM models for Effata Dutch.

Schema covers the six coaching modules:
  1. CurriculumWeek       -> Personalized Fluency Plan
  2. VocabTheme/VocabItem -> Core Vocabulary Accelerator
  3. GrammarTopic/Exercise-> Grammar Simplifier
  4. ConversationSession/Message -> Conversation Simulator
  5. (Pronunciation Coach is stateless DeepSeek calls, no dedicated table)
  6. SRSCard/ReviewLog    -> Memory Lock System (SM-2 spaced repetition)
"""
from __future__ import annotations

import datetime as dt
import enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


class CurriculumWeek(Base):
    __tablename__ = "curriculum_weeks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    week_number: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    goal: Mapped[str] = mapped_column(Text)
    module_focus: Mapped[str] = mapped_column(String(300))

    vocab_themes: Mapped[list["VocabTheme"]] = relationship(back_populates="week", cascade="all, delete-orphan")
    grammar_topics: Mapped[list["GrammarTopic"]] = relationship(back_populates="week", cascade="all, delete-orphan")


class VocabTheme(Base):
    __tablename__ = "vocab_themes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    week_id: Mapped[int] = mapped_column(ForeignKey("curriculum_weeks.id"))
    name: Mapped[str] = mapped_column(String(200))
    order: Mapped[int] = mapped_column(Integer, default=0)

    week: Mapped[CurriculumWeek] = relationship(back_populates="vocab_themes")
    items: Mapped[list["VocabItem"]] = relationship(back_populates="theme", cascade="all, delete-orphan")


class VocabItem(Base):
    __tablename__ = "vocab_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    theme_id: Mapped[int] = mapped_column(ForeignKey("vocab_themes.id"))
    dutch: Mapped[str] = mapped_column(String(200))
    english: Mapped[str] = mapped_column(String(200))
    ipa: Mapped[str] = mapped_column(String(200), default="")
    pronunciation_tip: Mapped[str] = mapped_column(Text, default="")
    example_nl: Mapped[str] = mapped_column(Text, default="")
    example_en: Mapped[str] = mapped_column(Text, default="")
    usage_context: Mapped[str] = mapped_column(Text, default="")

    theme: Mapped[VocabTheme] = relationship(back_populates="items")
    srs_cards: Mapped[list["SRSCard"]] = relationship(back_populates="vocab_item", cascade="all, delete-orphan")


class GrammarTopic(Base):
    __tablename__ = "grammar_topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    week_id: Mapped[int] = mapped_column(ForeignKey("curriculum_weeks.id"))
    title: Mapped[str] = mapped_column(String(200))
    explanation_md: Mapped[str] = mapped_column(Text)
    common_mistakes_md: Mapped[str] = mapped_column(Text, default="")
    order: Mapped[int] = mapped_column(Integer, default=0)

    week: Mapped[CurriculumWeek] = relationship(back_populates="grammar_topics")
    exercises: Mapped[list["GrammarExercise"]] = relationship(back_populates="topic", cascade="all, delete-orphan")


class GrammarExercise(Base):
    __tablename__ = "grammar_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("grammar_topics.id"))
    prompt: Mapped[str] = mapped_column(Text)
    choices_json: Mapped[str] = mapped_column(Text)  # JSON-encoded list[str]
    correct_index: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(Text, default="")

    topic: Mapped[GrammarTopic] = relationship(back_populates="exercises")
    srs_cards: Mapped[list["SRSCard"]] = relationship(back_populates="grammar_exercise", cascade="all, delete-orphan")


class ConversationDifficulty(str, enum.Enum):
    beginner = "beginner"
    elementary = "elementary"
    intermediate = "intermediate"


class ConversationSession(Base):
    __tablename__ = "conversation_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario: Mapped[str] = mapped_column(String(200), default="Algemeen gesprek")
    difficulty: Mapped[ConversationDifficulty] = mapped_column(
        Enum(ConversationDifficulty), default=ConversationDifficulty.beginner
    )
    started_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    messages: Mapped[list["ConversationMessage"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="ConversationMessage.created_at"
    )


class MessageRole(str, enum.Enum):
    user = "user"
    coach = "coach"


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("conversation_sessions.id"))
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole))
    content: Mapped[str] = mapped_column(Text)
    correction_note: Mapped[str] = mapped_column(Text, default="")  # gentle correction, coach messages only
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    session: Mapped[ConversationSession] = relationship(back_populates="messages")


class SRSCard(Base):
    """One spaced-repetition card, linked to either a vocab item or a grammar
    exercise (never both). SM-2 algorithm state lives directly on the row."""

    __tablename__ = "srs_cards"
    # Note: NOT a DB-level "exactly one of the two FKs is set" guarantee --
    # standard SQL treats NULL as distinct from NULL in unique indexes, so a
    # composite UNIQUE constraint here wouldn't actually enforce that
    # invariant. It's enforced at the application layer instead: app/seed.py
    # always creates exactly one SRSCard per vocab item or grammar exercise,
    # never both.

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vocab_item_id: Mapped[int | None] = mapped_column(ForeignKey("vocab_items.id"), nullable=True)
    grammar_exercise_id: Mapped[int | None] = mapped_column(ForeignKey("grammar_exercises.id"), nullable=True)

    ease_factor: Mapped[float] = mapped_column(Float, default=2.5)
    interval_days: Mapped[int] = mapped_column(Integer, default=0)
    repetitions: Mapped[int] = mapped_column(Integer, default=0)
    due_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    last_reviewed_at: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    vocab_item: Mapped[VocabItem | None] = relationship(back_populates="srs_cards")
    grammar_exercise: Mapped[GrammarExercise | None] = relationship(back_populates="srs_cards")
    review_logs: Mapped[list["ReviewLog"]] = relationship(back_populates="card", cascade="all, delete-orphan")


class ReviewLog(Base):
    __tablename__ = "review_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("srs_cards.id"))
    grade: Mapped[int] = mapped_column(Integer)  # 0-5, SM-2 quality score
    reviewed_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)

    card: Mapped[SRSCard] = relationship(back_populates="review_logs")


class LoginAttempt(Base):
    """Backing store for login rate limiting -- survives process restarts,
    unlike an in-memory counter, so a redeploy can't be used to reset lockouts."""

    __tablename__ = "login_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ip_address: Mapped[str] = mapped_column(String(64))
    success: Mapped[bool] = mapped_column(Boolean)
    attempted_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
