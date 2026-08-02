from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import generate_csrf_token, require_login
from app.config import get_settings
from app.db import get_db
from app.models import CurriculumWeek, VocabTheme
from app.templating import templates

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"], dependencies=[Depends(require_login)])
settings = get_settings()


@router.get("", response_class=HTMLResponse)
async def vocabulary_index(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CurriculumWeek)
        .options(selectinload(CurriculumWeek.vocab_themes).selectinload(VocabTheme.items))
        .order_by(CurriculumWeek.week_number)
    )
    weeks = [w for w in result.scalars().all() if w.vocab_themes]

    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse(
        "vocabulary.html", {"request": request, "weeks": weeks, "csrf_token": csrf_token}
    )
    response.set_cookie(
        "csrf_token", csrf_token, httponly=True, samesite="lax", secure=settings.is_production, max_age=3600
    )
    return response
