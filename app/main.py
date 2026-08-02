"""Effata Dutch -- application entrypoint.

Run locally:
    uvicorn app.main:app --reload

Production (Render):
    uvicorn app.main:app --host 0.0.0.0 --port $PORT
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import get_settings
from app.db import init_models
from app.routers import auth_router, conversation, dashboard, grammar, memory, pronunciation, vocabulary

settings = get_settings()


_INSECURE_DEFAULT_SECRET = "insecure-dev-secret-change-me"


def _assert_production_secrets_configured() -> None:
    """Fail fast on boot rather than silently signing session cookies with a
    known/default secret, or accepting a passcode nobody set. A crash on
    deploy is far cheaper than an authentication bypass in production."""
    if not settings.is_production:
        return
    problems = []
    if not settings.session_secret_key or settings.session_secret_key == _INSECURE_DEFAULT_SECRET:
        problems.append("SESSION_SECRET_KEY is missing or using the insecure default.")
    if len(settings.session_secret_key) < 32:
        problems.append("SESSION_SECRET_KEY is too short (use `secrets.token_urlsafe(48)`).")
    if not settings.app_passcode_hash:
        problems.append("APP_PASSCODE_HASH is not set.")
    if problems:
        raise RuntimeError(
            "Refusing to start in production with insecure configuration:\n- " + "\n- ".join(problems)
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    _assert_production_secrets_configured()
    # Table creation is idempotent (CREATE TABLE IF NOT EXISTS semantics via
    # SQLAlchemy metadata). Actual content seeding is a separate, explicit
    # step (`python -m app.seed`) run once via Render's release command --
    # keeping it out of the request-serving process's startup path avoids a
    # slow/flaky boot if the DB is briefly unreachable.
    await init_models()
    yield


app = FastAPI(title="Effata Dutch", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_router.router)
app.include_router(dashboard.router)
app.include_router(vocabulary.router)
app.include_router(grammar.router)
app.include_router(conversation.router)
app.include_router(pronunciation.router)
app.include_router(memory.router)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    # Defense-in-depth headers. No inline-script CSP relaxation is needed
    # since all JS is either external (HTMX from a pinned CDN URL) or in
    # static files -- keep 'unsafe-inline' out of script-src.
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' https://unpkg.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self'"
    )
    if settings.is_production:
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
    return response


@app.exception_handler(StarletteHTTPException)
async def redirect_unauthenticated(request: Request, exc: StarletteHTTPException):
    # require_login() raises a 303 with a Location header when the session
    # cookie is missing/invalid; let that redirect through untouched.
    if exc.status_code == 303 and exc.headers and "Location" in exc.headers:
        return RedirectResponse(url=exc.headers["Location"], status_code=303)
    from fastapi.exception_handlers import http_exception_handler

    return await http_exception_handler(request, exc)


@app.get("/healthz", response_class=HTMLResponse, include_in_schema=False)
async def healthz():
    return HTMLResponse("ok")
