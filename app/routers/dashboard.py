import datetime as dt

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import require_login
from app.db import get_db
from app.models import CurriculumWeek, SRSCard, User, VocabTheme
from app.templating import templates

router = APIRouter(tags=["dashboard"], dependencies=[Depends(require_login)])


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request, current_user: User = Depends(require_login), db: AsyncSession = Depends(get_db)
):
    weeks_result = await db.execute(
        select(CurriculumWeek)
        .options(selectinload(CurriculumWeek.vocab_themes).selectinload(VocabTheme.items))
        .order_by(CurriculumWeek.week_number)
    )
    weeks = weeks_result.scalars().all()

    mastered_ids_result = await db.execute(
        select(SRSCard.vocab_item_id).where(
            SRSCard.user_id == current_user.id,
            SRSCard.vocab_item_id.is_not(None),
            SRSCard.repetitions > 0,
        )
    )
    mastered_ids = set(mastered_ids_result.scalars().all())

    # A week unlocks once the previous week's vocab is fully mastered (or the
    # previous week has no vocab content seeded yet, so an empty stub week
    # never permanently blocks progression).
    week_rows = []
    prev_complete_or_empty = True
    for week in weeks:
        items = [item for theme in week.vocab_themes for item in theme.items]
        total = len(items)
        done = sum(1 for item in items if item.id in mastered_ids)
        complete = total == 0 or done == total
        week_rows.append({"week": week, "done": done, "total": total, "unlocked": prev_complete_or_empty})
        prev_complete_or_empty = complete

    due_count_result = await db.execute(
        select(func.count()).select_from(SRSCard).where(
            SRSCard.user_id == current_user.id,
            SRSCard.due_at <= dt.datetime.now(dt.timezone.utc),
        )
    )
    due_count = due_count_result.scalar_one()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "week_rows": week_rows, "due_count": due_count},
    )
