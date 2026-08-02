"""Multi-user passcode authentication.

Threat model: this app has a small, fixed set of legitimate users (household
members), provisioned by an operator via `python -m app.cli create-user` --
never through a public signup form. There is therefore no account-enumeration
surface worth defending in depth against (usernames aren't secret; the
passcode is). What remains in scope:

  - Passcodes must never be stored or compared in plaintext -> bcrypt via passlib.
  - Session token must be signed and tamper-evident -> itsdangerous, carrying
    the user's id as its subject.
  - Cookie must be HttpOnly + SameSite=Lax + Secure (in production) so it
    can't be read by JS (XSS) or replayed cross-site.
  - Login endpoint must be rate-limited per IP -> LoginAttempt table, so an
    attacker can't brute-force a short passcode.
  - Every state-changing form must carry a CSRF token, since we rely on
    cookies rather than a bearer token for auth.
  - Every per-user resource (SRS cards, conversation sessions) must be loaded
    scoped to the requesting user's id, and ownership re-checked on mutation
    -- a valid session for user A must never let them touch user B's data by
    guessing an id.
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
from app.models import LoginAttempt, User

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_serializer = URLSafeTimedSerializer(settings.session_secret_key, salt="effata-dutch-session")


def hash_passcode(plaintext: str) -> str:
    return pwd_context.hash(plaintext)


def verify_user_passcode(user: User, plaintext: str) -> bool:
    return pwd_context.verify(plaintext, user.passcode_hash)


def normalize_username(username: str) -> str:
    return username.strip().lower()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == normalize_username(username)))
    return result.scalars().first()


def create_session_token(user_id: int) -> str:
    return _serializer.dumps(user_id)


def read_session_token(token: str) -> int | None:
    """Returns the user id encoded in the token, or None if the token is
    missing, expired, tampered with, or not shaped like a user id."""
    try:
        subject = _serializer.loads(token, max_age=settings.session_max_age_seconds)
    except BadSignature:
        return None
    if not isinstance(subject, int):
        return None
    return subject


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


async def require_login(request: Request, db: AsyncSession = Depends(get_db)) -> User:
    """Resolves the session cookie to a User row, 303-redirecting to /login if
    absent/invalid/stale. Stashes the user on request.state so base.html can
    render the display name without every route threading it through."""
    token = request.cookies.get(settings.session_cookie_name)
    user_id = read_session_token(token) if token else None
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})

    user = await db.get(User, user_id)
    if user is None:
        # Session signed for a user that no longer exists (deleted account) --
        # treat exactly like "not logged in", don't leak which case it was.
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})

    request.state.user = user
    return user


async def verify_csrf(request: Request, csrf_token: str = "") -> None:
    expected = request.cookies.get("csrf_token")
    if not expected or not csrf_token or not hmac.compare_digest(expected, csrf_token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")


DbDep = Depends(get_db)
