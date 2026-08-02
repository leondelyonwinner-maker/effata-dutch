import json

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import generate_csrf_token, require_login, verify_csrf
from app.config import get_settings
from app.db import get_db
from app.models import CurriculumWeek, GrammarExercise, GrammarTopic
from app.templating import templates

router = APIRouter(prefix="/grammar", tags=["grammar"], dependencies=[Depends(require_login)])
settings = get_settings()


@router.get("", response_class=HTMLResponse)
async def grammar_index(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CurriculumWeek)
        .options(selectinload(CurriculumWeek.grammar_topics).selectinload(GrammarTopic.exercises))
        .order_by(CurriculumWeek.week_number)
    )
    weeks = [w for w in result.scalars().all() if w.grammar_topics]

    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse(
        "grammar.html", {"request": request, "weeks": weeks, "csrf_token": csrf_token}
    )
    response.set_cookie(
        "csrf_token", csrf_token, httponly=True, samesite="lax", secure=settings.is_production, max_age=3600
    )
    return response


@router.post("/exercise/{exercise_id}/check", response_class=HTMLResponse)
async def check_exercise(
    exercise_id: int,
    request: Request,
    answer_index: int = Form(...),
    csrf_token: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    await verify_csrf(request, csrf_token)

    exercise = await db.get(GrammarExercise, exercise_id)
    if exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")

    is_correct = answer_index == exercise.correct_index
    choices = json.loads(exercise.choices_json)

    return templates.TemplateResponse(
        "partials/exercise_result.html",
        {
            "request": request,
            "is_correct": is_correct,
            "explanation": exercise.explanation,
            "correct_choice": choices[exercise.correct_index],
        },
    )
