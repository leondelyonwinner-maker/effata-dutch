"""Shared XP/streak bookkeeping for the Voortgang (progress) tab.

Kept as one small module rather than duplicated inline in each router that
can award XP (SRS grading today; curriculum module completion later) so the
streak rule only lives in one place.
"""
from __future__ import annotations

import datetime as dt

from app.models import User

# Matches the SM-2 grade scale used elsewhere (0-5): >=3 counts as a
# successful recall for XP/streak purposes, same cutoff SM-2 itself uses to
# decide whether repetitions advance or reset.
KNOWN_GRADE_THRESHOLD = 3
XP_KNOWN = 10
XP_UNKNOWN = 2


def bump_streak_and_xp(user: User, *, xp_delta: int) -> None:
    """Mutates user.xp/streak_days/last_study_date in place. Caller is
    responsible for committing the session."""
    user.xp = max(0, user.xp + xp_delta)

    today = dt.datetime.now(dt.timezone.utc).date()
    if user.last_study_date == today:
        return  # streak already counted for today
    yesterday = today - dt.timedelta(days=1)
    user.streak_days = user.streak_days + 1 if user.last_study_date == yesterday else 1
    user.last_study_date = today
