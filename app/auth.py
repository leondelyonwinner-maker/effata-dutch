"""Single-user passcode authentication.

Threat model: this app has exactly one legitimate user (Leo). There is no
signup flow and therefore no account-enumeration or password-reset attack
surface to worry about. What remains in scope:

  - Passcode must never be stored or compared in plaintext -> bcrypt via passlib.
  - Session token must be signed and tamper-evident -> itsdangerous.
  - Cookie must be HttpOnly + SameSite=Lax + Secure (in production) so it
    can't be read by JS (XSS) or replayed cross-site.
  - Login endpoint must be rate-limited per IP -> LoginAttempt table, so an
    attacker can't brute-force a short passcode.
  - Every state-changing form must carry a CSRF token, since we rely on
    cookies rather than a bearer token for auth.
"""
from __future__ import annotations

import datetime as dt
import hmac
import secrets

from fastapi import Depends, HTTPException, Request, status
from itsdangerous import BadSignature, URLSafeTimedSerializer
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.db import get_db
from app.models import LoginAttempt

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_serializer = URLSafeTimedSerializer(settings.session_secret_key, salt="effata-dutch-session")

SESSION_SUBJECT = "authenticated"


def hash_passcode(plaintext: str) -> str:
    return pwd_context.hash(plaintext)


def verify_passcode(plaintext: str) -> bool:
    if not settings.app_passcode_hash:
        # Fail closed: an unconfigured passcode must never mean "let everyone in".
        return False
    return pwd_context.verify(plaintext, settings.app_passcode_hash)


def create_session_token() -> str:
    return _serializer.dumps(SESSION_SUBJECT)


def read_session_token(token: str) -> bool:
    try:
        subject = _serializer.loads(token, max_age=settings.session_max_age_seconds)
    except BadSignature:
        return False
    return hmac.compare_digest(subject, SESSION_SUBJECT)


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


async def is_ip_locked_out(db: AsyncSession, ip_address: str) -> bool:
    window_start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=settings.login_lockout_seconds)
    stmt = select(func.count()).select_from(LoginAttempt).where(
        LoginAttempt.ip_address == ip_address,
        LoginAttempt.success.is_(False),
        LoginAttempt.attempted_at >= window_start,
    )
    result = await db.execute(stmt)
    failed_count = result.scalar_one()
    return failed_count >= settings.login_max_attempts


async def record_login_attempt(db: AsyncSession, ip_address: str, success: bool) -> None:
    db.add(LoginAttempt(ip_address=ip_address, success=success))
    await db.commit()


def client_ip(request: Request) -> str:
    # Render sits behind a proxy; X-Forwarded-For's first hop is the real client.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def require_login(request: Request) -> None:
    token = request.cookies.get(settings.session_cookie_name)
    if not token or not read_session_token(token):
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})


def is_authenticated(request: Request) -> bool:
    token = request.cookies.get(settings.session_cookie_name)
    return bool(token and read_session_token(token))


async def verify_csrf(request: Request, csrf_token: str = "") -> None:
    expected = request.cookies.get("csrf_token")
    if not expected or not csrf_token or not hmac.compare_digest(expected, csrf_token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")


DbDep = Depends(get_db)
