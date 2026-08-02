from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import require_login
from app.db import get_db
from app.models import CurriculumWeek, PronunciationAttempt, SRSCard, User, VocabItem, VocabTheme
from app.templating import templates

router = APIRouter(prefix="/progress", tags=["progress"], dependencies=[Depends(require_login)])


def _level_for_xp(xp: int) -> str:
    if xp < 100:
        return "A0"
    if xp < 400:
        return "A1"
    return "A2"


@router.get("", response_class=HTMLResponse)
async def progress_page(
    request: Request, current_user: User = Depends(require_login), db: AsyncSession = Depends(get_db)
):
    total_words = (await db.execute(select(func.count()).select_from(VocabItem))).scalar_one()

    mastered_ids_result = await db.execute(
        select(SRSCard.vocab_item_id).where(
            SRSCard.user_id == current_user.id,
            SRSCard.vocab_item_id.is_not(None),
            SRSCard.repetitions > 0,
        )
    )
    mastered_ids = set(mastered_ids_result.scalars().all())

    # Curriculum "done" = every vocab item in that week has been recalled at
    # least once via SRS. Grammar exercises aren't folded in here -- there's
    # no persisted per-attempt correctness log for them yet (grammar.py's
    # check is stateless), so mixing them in would silently mis-weight the
    # bar. Vocabulary mastery alone is an honest, if partial, progress signal.
    weeks = (
        (
            await db.execute(
                select(CurriculumWeek)
                .options(selectinload(CurriculumWeek.vocab_themes).selectinload(VocabTheme.items))
                .order_by(CurriculumWeek.week_number)
            )
        )
        .scalars()
        .all()
    )

    week_progress = []
    done_weeks = 0
    for week in weeks:
        items = [item for theme in week.vocab_themes for item in theme.items]
        total = len(items)
        done = sum(1 for item in items if item.id in mastered_ids)
        complete = total > 0 and done == total
        if complete:
            done_weeks += 1
        week_progress.append({"week": week, "done": done, "total": total, "complete": complete})

    pron_avg, pron_count = (
        await db.execute(
            select(func.avg(PronunciationAttempt.score), func.count(PronunciationAttempt.id)).where(
                PronunciationAttempt.user_id == current_user.id
            )
        )
    ).one()

    all_vocab = (await db.execute(select(VocabItem).order_by(VocabItem.id))).scalars().all()

    return templates.TemplateResponse(
        "progress.html",
        {
            "request": request,
            "streak_days": current_user.streak_days,
            "xp": current_user.xp,
            "level": _level_for_xp(current_user.xp),
            "words_mastered": len(mastered_ids),
            "total_words": total_words,
            "week_progress": week_progress,
            "total_weeks": len(weeks),
            "done_weeks": done_weeks,
            "pron_avg": round(pron_avg) if pron_avg is not None else None,
            "pron_count": pron_count or 0,
            "all_vocab": all_vocab,
            "mastered_ids": mastered_ids,
        },
    )
