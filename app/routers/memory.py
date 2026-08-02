import datetime as dt
import json

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import generate_csrf_token, require_login, verify_csrf
from app.config import get_settings
from app.db import get_db
from app.models import SRSCard, ReviewLog
from app.srs import schedule_next_review
from app.templating import templates

router = APIRouter(prefix="/memory", tags=["memory"], dependencies=[Depends(require_login)])
settings = get_settings()


async def _due_card(db: AsyncSession) -> SRSCard | None:
    now = dt.datetime.now(dt.timezone.utc)
    result = await db.execute(
        select(SRSCard)
        .options(selectinload(SRSCard.vocab_item), selectinload(SRSCard.grammar_exercise))
        .where(SRSCard.due_at <= now)
        .order_by(SRSCard.due_at)
        .limit(1)
    )
    return result.scalars().first()


async def _card_context(db: AsyncSession) -> dict:
    card = await _due_card(db)
    front, back, card_type = None, None, None
    if card is not None:
        if card.vocab_item is not None:
            card_type = "vocab"
            front = card.vocab_item.dutch
            back = f"{card.vocab_item.english} — {card.vocab_item.example_nl}"
        elif card.grammar_exercise is not None:
            card_type = "grammar"
            choices = json.loads(card.grammar_exercise.choices_json)
            front = card.grammar_exercise.prompt
            back = f"{choices[card.grammar_exercise.correct_index]} — {card.grammar_exercise.explanation}"
    return {"card": card, "front": front, "back": back, "card_type": card_type}


@router.get("", response_class=HTMLResponse)
async def review_queue(request: Request, db: AsyncSession = Depends(get_db)):
    csrf_token = generate_csrf_token()
    context = await _card_context(db)
    response = templates.TemplateResponse(
        "memory.html", {"request": request, "csrf_token": csrf_token, **context}
    )
    response.set_cookie(
        "csrf_token", csrf_token, httponly=True, samesite="lax", secure=settings.is_production, max_age=3600
    )
    return response


@router.post("/card/{card_id}/grade", response_class=HTMLResponse)
async def grade_card(
    card_id: int,
    request: Request,
    grade: int = Form(...),
    csrf_token: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    await verify_csrf(request, csrf_token)

    if not 0 <= grade <= 5:
        raise HTTPException(status_code=422, detail="grade must be 0-5")

    card = await db.get(SRSCard, card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    schedule_next_review(card, grade)
    db.add(ReviewLog(card_id=card.id, grade=grade))
    await db.commit()

    # Respond with just the review-card fragment (HTMX outerHTML swap target),
    # not the full page -- re-fetching CSRF token since the form that triggered
    # this POST doesn't carry a fresh one for the next card.
    new_csrf_token = generate_csrf_token()
    context = await _card_context(db)
    response = templates.TemplateResponse(
        "partials/review_card.html", {"request": request, "csrf_token": new_csrf_token, **context}
    )
    response.set_cookie(
        "csrf_token", new_csrf_token, httponly=True, samesite="lax", secure=settings.is_production, max_age=3600
    )
    return response
