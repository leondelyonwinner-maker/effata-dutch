from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import generate_csrf_token, require_login, verify_csrf
from app.config import get_settings
from app.db import get_db
from app.deepseek_client import COACH_PERSONA, SCENARIO_KICKOFF_HINTS, DeepSeekError, chat_completion
from app.models import ConversationDifficulty, ConversationMessage, ConversationSession, MessageRole, User
from app.templating import templates

router = APIRouter(prefix="/conversation", tags=["conversation"], dependencies=[Depends(require_login)])
settings = get_settings()

# The six domains from the coaching brief. Order doubles as the rotation
# order the coach persona is nudged toward when the learner doesn't pick one.
SCENARIOS = list(SCENARIO_KICKOFF_HINTS.keys())
DEFAULT_SCENARIO = SCENARIOS[2]  # "Dagelijks gesprek" -- least intimidating default for a cold start

# Bump difficulty every N user turns so the conversation ramps up gradually,
# per the coaching brief ("gradually increase difficulty").
TURNS_PER_DIFFICULTY_STEP = 6
DIFFICULTY_ORDER = [
    ConversationDifficulty.beginner,
    ConversationDifficulty.elementary,
    ConversationDifficulty.intermediate,
]

# Used only if DeepSeek is unreachable when a session is created -- so a new
# session never opens on a dead, empty chat log.
FALLBACK_OPENERS: dict[str, str] = {
    "Werk & Engineering": "Hallo! Laten we het over werk hebben. Waar werk je aan deze week? "
    "(Let's talk about work. What are you working on this week?)",
    "Presentatie geven": "Hallo! Stel je voor dat je een update geeft aan je team. Waarover gaat je project? "
    "(Imagine you're giving your team an update. What's your project about?)",
    "Dagelijks gesprek": "Hallo! Hoe gaat het met je vandaag? "
    "(Hello! How are you doing today?)",
    "Boodschappen doen": "Hallo! We zijn in de supermarkt. Wat wil je kopen? "
    "(We're at the supermarket. What do you want to buy?)",
    "Gemeenschap & vrienden": "Hallo! Je bent net op een buurtborrel aangekomen. Hoe stel je jezelf voor? "
    "(You've just arrived at a neighborhood get-together. How do you introduce yourself?)",
    "Preken in de kerk": "Hallo! Stel je voor dat je de gemeente welkom heet voor de dienst. Hoe begin je? "
    "(Imagine welcoming the congregation before the service. How do you start?)",
}


def _next_difficulty(user_turn_count: int, current: ConversationDifficulty) -> ConversationDifficulty:
    step = min(user_turn_count // TURNS_PER_DIFFICULTY_STEP, len(DIFFICULTY_ORDER) - 1)
    return DIFFICULTY_ORDER[step]


async def _generate_opening_message(scenario: str, difficulty: ConversationDifficulty) -> str:
    hint = SCENARIO_KICKOFF_HINTS.get(scenario, scenario)
    system = COACH_PERSONA + f"\nCurrent difficulty level: {difficulty.value}."
    kickoff_instruction = (
        f"Start a brand-new conversation session. The scenario domain is '{scenario}': {hint}. "
        "Open with a short, welcoming line in Dutch (with an English gloss in parentheses for any "
        "new vocabulary), set the scene in one short sentence, and end with one question that "
        "invites the learner to respond within this scenario."
    )
    try:
        return await chat_completion(
            [
                {"role": "system", "content": system},
                {"role": "user", "content": kickoff_instruction},
            ]
        )
    except DeepSeekError:
        return FALLBACK_OPENERS.get(scenario, FALLBACK_OPENERS[DEFAULT_SCENARIO])


async def _create_session(db: AsyncSession, user_id: int, scenario: str) -> ConversationSession:
    # Carry the learner's difficulty forward from their most recent session
    # rather than resetting to beginner every time they switch topics.
    prev_result = await db.execute(
        select(ConversationSession.difficulty)
        .where(ConversationSession.user_id == user_id)
        .order_by(ConversationSession.started_at.desc())
        .limit(1)
    )
    difficulty = prev_result.scalars().first() or ConversationDifficulty.beginner

    session = ConversationSession(user_id=user_id, scenario=scenario, difficulty=difficulty)
    db.add(session)
    await db.flush()

    opening = await _generate_opening_message(scenario, difficulty)
    db.add(ConversationMessage(session_id=session.id, role=MessageRole.coach, content=opening))
    await db.commit()
    await db.refresh(session, attribute_names=["messages"])
    return session


async def _get_or_create_session(db: AsyncSession, user_id: int) -> ConversationSession:
    result = await db.execute(
        select(ConversationSession)
        .options(selectinload(ConversationSession.messages))
        .where(ConversationSession.user_id == user_id)
        .order_by(ConversationSession.started_at.desc())
        .limit(1)
    )
    session = result.scalars().first()
    if session is None:
        session = await _create_session(db, user_id, DEFAULT_SCENARIO)
    return session


@router.get("", response_class=HTMLResponse)
async def conversation_page(
    request: Request, current_user: User = Depends(require_login), db: AsyncSession = Depends(get_db)
):
    session = await _get_or_create_session(db, current_user.id)
    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse(
        "conversation.html",
        {
            "request": request,
            "session": session,
            "csrf_token": csrf_token,
            "error": None,
            "scenarios": SCENARIOS,
        },
    )
    response.set_cookie(
        "csrf_token", csrf_token, httponly=True, samesite="lax", secure=settings.is_production, max_age=3600
    )
    return response


@router.post("/new")
async def start_new_topic(
    request: Request,
    scenario: str = Form(...),
    csrf_token: str = Form(...),
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_db),
):
    """'Ganti topik' -- deliberately starts a fresh conversation thread in a
    chosen domain, instead of the learner being stuck in one open-ended chat
    forever. Coach Effata opens the new thread with a scenario-specific line."""
    await verify_csrf(request, csrf_token)
    if scenario not in SCENARIOS:
        raise HTTPException(status_code=422, detail="Unknown scenario")

    await _create_session(db, current_user.id, scenario)
    return RedirectResponse(url="/conversation", status_code=303)


@router.post("/{session_id}/message", response_class=HTMLResponse)
async def send_message(
    session_id: int,
    request: Request,
    content: str = Form(..., min_length=1, max_length=2000),
    csrf_token: str = Form(...),
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_db),
):
    await verify_csrf(request, csrf_token)

    result = await db.execute(
        select(ConversationSession)
        .options(selectinload(ConversationSession.messages))
        .where(ConversationSession.id == session_id)
    )
    session = result.scalars().first()
    # 404 for both "doesn't exist" and "belongs to someone else" -- a
    # guessed session_id shouldn't let a caller post into another user's chat.
    if session is None or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation session not found")

    # Build the DeepSeek history *before* persisting the user turn, then
    # commit the user's message immediately -- so if the DeepSeek call fails,
    # the learner's own message is never lost.
    user_turn_count = sum(1 for m in session.messages if m.role == MessageRole.user) + 1
    new_difficulty = _next_difficulty(user_turn_count, session.difficulty)
    session.difficulty = new_difficulty

    hint = SCENARIO_KICKOFF_HINTS.get(session.scenario, session.scenario)
    system = (
        COACH_PERSONA
        + f"\nCurrent difficulty level: {new_difficulty.value}."
        + f"\nThis session's scenario domain is '{session.scenario}': {hint}. Stay within or "
        "naturally build on this scenario unless the learner clearly steers elsewhere."
    )
    history = [{"role": "system", "content": system}]
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
