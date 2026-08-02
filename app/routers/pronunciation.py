import json

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse

from app.auth import generate_csrf_token, require_login, verify_csrf
from app.config import get_settings
from app.deepseek_client import PRONUNCIATION_SYSTEM_PROMPT, DeepSeekError, chat_completion
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
