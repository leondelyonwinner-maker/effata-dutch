"""SM-2 spaced repetition scheduling (SuperMemo 2 algorithm).

Grades are 0-5:
  0-2 = failed recall (card is reset)
  3-5 = successful recall, quality increases the ease factor
"""
from __future__ import annotations

import datetime as dt

from app.models import SRSCard


def schedule_next_review(card: SRSCard, grade: int) -> SRSCard:
    if not 0 <= grade <= 5:
        raise ValueError("grade must be between 0 and 5")

    now = dt.datetime.now(dt.timezone.utc)

    if grade < 3:
        # Failed recall: reset repetitions but keep the ease factor decay
        # so a consistently-hard card converges to more frequent review.
        card.repetitions = 0
        card.interval_days = 1
    else:
        if card.repetitions == 0:
            card.interval_days = 1
        elif card.repetitions == 1:
            card.interval_days = 6
        else:
            card.interval_days = round(card.interval_days * card.ease_factor)
        card.repetitions += 1

    new_ease = card.ease_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
    card.ease_factor = max(1.3, new_ease)

    card.last_reviewed_at = now
    card.due_at = now + dt.timedelta(days=card.interval_days)
    return card
