from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import require_login
from app.db import get_db
from app.models import CurriculumWeek, VocabTheme
from app.templating import templates

router = APIRouter(prefix="/vocabulary", tags=["vocabulary"], dependencies=[Depends(require_login)])


@router.get("", response_class=HTMLResponse)
async def vocabulary_index(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(CurriculumWeek)
        .options(selectinload(CurriculumWeek.vocab_themes).selectinload(VocabTheme.items))
        .order_by(CurriculumWeek.week_number)
    )
    weeks = [w for w in result.scalars().all() if w.vocab_themes]
    return templates.TemplateResponse("vocabulary.html", {"request": request, "weeks": weeks})
