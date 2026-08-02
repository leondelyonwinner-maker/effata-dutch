import datetime as dt

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import require_login
from app.db import get_db
from app.models import CurriculumWeek, SRSCard
from app.templating import templates

router = APIRouter(tags=["dashboard"], dependencies=[Depends(require_login)])


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    weeks_result = await db.execute(select(CurriculumWeek).order_by(CurriculumWeek.week_number))
    weeks = weeks_result.scalars().all()

    due_count_result = await db.execute(
        select(func.count()).select_from(SRSCard).where(SRSCard.due_at <= dt.datetime.now(dt.timezone.utc))
    )
    due_count = due_count_result.scalar_one()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "weeks": weeks, "due_count": due_count},
    )
