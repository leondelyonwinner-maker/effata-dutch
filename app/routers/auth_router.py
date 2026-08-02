from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import (
    client_ip,
    create_session_token,
    generate_csrf_token,
    get_user_by_username,
    is_ip_locked_out,
    record_login_attempt,
    verify_csrf,
    verify_user_passcode,
)
from app.config import get_settings
from app.db import get_db
from app.templating import templates

router = APIRouter(tags=["auth"])
settings = get_settings()


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse(
        "login.html", {"request": request, "csrf_token": csrf_token, "error": None, "username_value": ""}
    )
    response.set_cookie(
        "csrf_token",
        csrf_token,
        httponly=True,
        samesite="lax",
        secure=settings.is_production,
        max_age=600,
    )
    return response


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    passcode: str = Form(...),
    csrf_token: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    await verify_csrf(request, csrf_token)
    ip = client_ip(request)

    if await is_ip_locked_out(db, ip):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "csrf_token": csrf_token,
                "error": "Too many failed attempts. Please wait a few minutes before trying again.",
                "username_value": username,
            },
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )

    user = await get_user_by_username(db, username)
    if user is None or not verify_user_passcode(user, passcode):
        await record_login_attempt(db, ip, success=False)
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "csrf_token": csrf_token,
                "error": "Incorrect username or passcode.",
                "username_value": username,
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    await record_login_attempt(db, ip, success=True)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        settings.session_cookie_name,
        create_session_token(user.id),
        httponly=True,
        samesite="lax",
        secure=settings.is_production,
        max_age=settings.session_max_age_seconds,
    )
    response.delete_cookie("csrf_token")
    return response


@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(settings.session_cookie_name)
    return response
