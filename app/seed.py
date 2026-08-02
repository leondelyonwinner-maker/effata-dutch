"""Idempotent seeding: safe to run on every deploy (checks before inserting).

Seeds curriculum content only (weeks, vocab, grammar) -- it deliberately does
NOT create SRSCard rows, because SRS cards are scoped per user and this
script runs before any user necessarily exists (Render's preDeployCommand
runs it ahead of the operator ever running `app.cli create-user`). Run
`python -m app.cli create-user ...` for each learner after this, which
backfills their SRS cards automatically; run `python -m app.cli
sync-srs-cards` after seeding *new* content into an app that already has
users, to backfill cards for the new items across everyone.
"""
from __future__ import annotations

import asyncio
import json

from sqlalchemy import select

from app.db import AsyncSessionLocal, init_models
from app.models import CurriculumWeek, GrammarExercise, GrammarTopic, VocabItem, VocabTheme
from app.seed_data import (
    CURRICULUM,
    WEEK_1_GRAMMAR_TOPICS,
    WEEK_1_VOCAB_THEMES,
    WEEK_2_VOCAB_THEMES,
    WEEK_6_VOCAB_THEMES,
    WEEK_7_VOCAB_THEMES,
    WEEK_9_VOCAB_THEMES,
)

# Maps week_number -> that week's vocab themes. Grammar content only exists
# for week 1 so far (see seed_data.py module docstring for what's stubbed).
VOCAB_BY_WEEK: dict[int, list[dict]] = {
    1: WEEK_1_VOCAB_THEMES,
    2: WEEK_2_VOCAB_THEMES,
    6: WEEK_6_VOCAB_THEMES,
    7: WEEK_7_VOCAB_THEMES,
    9: WEEK_9_VOCAB_THEMES,
}


async def seed() -> None:
    await init_models()
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(CurriculumWeek))
        if existing.scalars().first() is not None:
            print("Seed data already present -- skipping.")
            return

        week_rows: dict[int, CurriculumWeek] = {}
        for week in CURRICULUM:
            row = CurriculumWeek(**week)
            db.add(row)
            week_rows[week["week_number"]] = row
        await db.flush()

        for week_number, vocab_themes in VOCAB_BY_WEEK.items():
            week_row = week_rows[week_number]
            for theme_order, theme_data in enumerate(vocab_themes):
                theme = VocabTheme(week_id=week_row.id, name=theme_data["name"], order=theme_order)
                db.add(theme)
                await db.flush()
                for item_data in theme_data["items"]:
                    item = VocabItem(theme_id=theme.id, **item_data)
                    db.add(item)

        week_1 = week_rows[1]
        for topic_order, topic_data in enumerate(WEEK_1_GRAMMAR_TOPICS):
            topic = GrammarTopic(
                week_id=week_1.id,
                title=topic_data["title"],
                explanation_md=topic_data["explanation_md"],
                common_mistakes_md=topic_data["common_mistakes_md"],
                order=topic_order,
            )
            db.add(topic)
            await db.flush()
            for ex_data in topic_data["exercises"]:
                exercise = GrammarExercise(
                    topic_id=topic.id,
                    prompt=ex_data["prompt"],
                    choices_json=json.dumps(ex_data["choices"]),
                    correct_index=ex_data["correct_index"],
                    explanation=ex_data["explanation"],
                )
                db.add(exercise)

        await db.commit()
        seeded_weeks = ", ".join(str(n) for n in sorted(VOCAB_BY_WEEK))
        print(
            f"Seed complete: 10-week roadmap loaded, vocab seeded for weeks {seeded_weeks}, "
            "grammar seeded for week 1. Now run `python -m app.cli create-user ...` for each learner."
        )


if __name__ == "__main__":
    asyncio.run(seed())
