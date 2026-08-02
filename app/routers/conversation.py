from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import generate_csrf_token, require_login, verify_csrf
from app.config import get_settings
from app.db import get_db
from app.deepseek_client import COACH_PERSONA, DeepSeekError, chat_completion
from app.models import ConversationDifficulty, ConversationMessage, ConversationSession, MessageRole
from app.templating import templates

router = APIRouter(prefix="/conversation", tags=["conversation"], dependencies=[Depends(require_login)])
settings = get_settings()

# Bump difficulty every N user turns so the conversation ramps up gradually,
# per the coaching brief ("gradually increase difficulty").
TURNS_PER_DIFFICULTY_STEP = 6
DIFFICULTY_ORDER = [
    ConversationDifficulty.beginner,
    ConversationDifficulty.elementary,
    ConversationDifficulty.intermediate,
]


async def _get_or_create_session(db: AsyncSession) -> ConversationSession:
    result = await db.execute(
        select(ConversationSession)
        .options(selectinload(ConversationSession.messages))
        .order_by(ConversationSession.started_at.desc())
        .limit(1)
    )
    session = result.scalars().first()
    if session is None:
        session = ConversationSession()
        db.add(session)
        await db.commit()
        await db.refresh(session, attribute_names=["messages"])
    return session


def _next_difficulty(user_turn_count: int, current: ConversationDifficulty) -> ConversationDifficulty:
    step = min(user_turn_count // TURNS_PER_DIFFICULTY_STEP, len(DIFFICULTY_ORDER) - 1)
    return DIFFICULTY_ORDER[step]


@router.get("", response_class=HTMLResponse)
async def conversation_page(request: Request, db: AsyncSession = Depends(get_db)):
    session = await _get_or_create_session(db)
    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse(
        "conversation.html",
        {"request": request, "session": session, "csrf_token": csrf_token, "error": None},
    )
    response.set_cookie(
        "csrf_token", csrf_token, httponly=True, samesite="lax", secure=settings.is_production, max_age=3600
    )
    return response


@router.post("/{session_id}/message", response_class=HTMLResponse)
async def send_message(
    session_id: int,
    request: Request,
    content: str = Form(..., min_length=1, max_length=2000),
    csrf_token: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    await verify_csrf(request, csrf_token)

    result = await db.execute(
        select(ConversationSession)
        .options(selectinload(ConversationSession.messages))
        .where(ConversationSession.id == session_id)
    )
    session = result.scalars().first()
    if session is None:
        raise HTTPException(status_code=404, detail="Conversation session not found")

    # Build the DeepSeek history *before* persisting the user turn, then
    # commit the user's message immediately -- so if the DeepSeek call fails,
    # Leo's own message is never lost.
    user_turn_count = sum(1 for m in session.messages if m.role == MessageRole.user) + 1
    new_difficulty = _next_difficulty(user_turn_count, session.difficulty)
    session.difficulty = new_difficulty

    history = [{"role": "system", "content": COACH_PERSONA + f"\nCurrent difficulty level: {new_difficulty.value}."}]
    for m in session.messages:
        role = "user" if m.role == MessageRole.user else "assistant"
        history.append({"role": role, "content": m.content})
    history.append({"role": "user", "content": content.strip()})

    user_message = ConversationMessage(session_id=session.id, role=MessageRole.user, content=content.strip())
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)

    error = None
    coach_message = None
    try:
        reply = await chat_completion(history)
        coach_message = ConversationMessage(session_id=session.id, role=MessageRole.coach, content=reply)
        db.add(coach_message)
        await db.commit()
        await db.refresh(coach_message)
    except DeepSeekError as exc:
        error = str(exc)

    return templates.TemplateResponse(
        "partials/conversation_turn.html",
        {"request": request, "user_message": user_message, "coach_message": coach_message, "error": error},
    )
