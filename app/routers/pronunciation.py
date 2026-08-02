import json

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import generate_csrf_token, require_login, verify_csrf
from app.config import get_settings
from app.db import get_db
from app.deepseek_client import PRONUNCIATION_SYSTEM_PROMPT, DeepSeekError, chat_completion
from app.models import PronunciationAttempt, User
from app.pronunciation_scoring import score_pronunciation, score_tier, word_diff
from app.templating import templates

router = APIRouter(prefix="/pronunciation", tags=["pronunciation"], dependencies=[Depends(require_login)])
settings = get_settings()


@router.get("", response_class=HTMLResponse)
async def pronunciation_page(request: Request):
    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse(
        "pronunciation.html", {"request": request, "csrf_token": csrf_token, "result": None, "error": None, "text": ""}
    )
    response.set_cookie(
        "csrf_token", csrf_token, httponly=True, samesite="lax", secure=settings.is_production, max_age=3600
    )
    return response


@router.post("/check", response_class=HTMLResponse)
async def check_pronunciation(
    request: Request,
    text: str = Form(..., min_length=1, max_length=300),
    csrf_token: str = Form(...),
):
    await verify_csrf(request, csrf_token)

    result, error = None, None
    try:
        raw = await chat_completion(
            [
                {"role": "system", "content": PRONUNCIATION_SYSTEM_PROMPT},
                {"role": "user", "content": text.strip()},
            ],
            temperature=0.2,
            json_mode=True,
        )
        result = json.loads(raw)
    except DeepSeekError as exc:
        error = str(exc)
    except (json.JSONDecodeError, TypeError):
        error = "Coach Effata returned an unexpected format. Please try again."

    return templates.TemplateResponse(
        "partials/pronunciation_result.html", {"request": request, "result": result, "error": error, "text": text}
    )


@router.post("/score", response_class=HTMLResponse)
async def score_attempt(
    request: Request,
    target_text: str = Form(..., min_length=1, max_length=300),
    transcript: str = Form(..., min_length=0, max_length=300),
    csrf_token: str = Form(...),
    current_user: User = Depends(require_login),
    db: AsyncSession = Depends(get_db),
):
    """Scores a browser-transcribed 'Ucapkan kata ini' attempt against the
    target text (see app/pronunciation_scoring.py for what this can and
    can't measure) and logs it to the user's Voortgang accuracy average.
    The audio itself never reaches the server -- only the browser's own
    transcript does."""
    await verify_csrf(request, csrf_token)

    score = score_pronunciation(target_text, transcript)
    diff = word_diff(target_text, transcript)
    tier = score_tier(score)

    db.add(
        PronunciationAttempt(
            user_id=current_user.id,
            target_text=target_text.strip()[:300],
            transcript=transcript.strip()[:300],
            score=score,
        )
    )
    await db.commit()

    return templates.TemplateResponse(
        "partials/pronunciation_score_result.html",
        {"request": request, "score": score, "tier": tier, "diff": diff, "transcript": transcript},
    )
