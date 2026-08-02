"""Idempotent seeding: safe to run on every deploy (checks before inserting)."""
from __future__ import annotations

import asyncio
import json

from sqlalchemy import select

from app.db import AsyncSessionLocal, init_models
from app.models import CurriculumWeek, GrammarExercise, GrammarTopic, SRSCard, VocabItem, VocabTheme
from app.seed_data import CURRICULUM, WEEK_1_GRAMMAR_TOPICS, WEEK_1_VOCAB_THEMES


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

        week_1 = week_rows[1]

        for theme_order, theme_data in enumerate(WEEK_1_VOCAB_THEMES):
            theme = VocabTheme(week_id=week_1.id, name=theme_data["name"], order=theme_order)
            db.add(theme)
            await db.flush()
            for item_data in theme_data["items"]:
                item = VocabItem(theme_id=theme.id, **item_data)
                db.add(item)
                await db.flush()
                db.add(SRSCard(vocab_item_id=item.id))

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
                await db.flush()
                db.add(SRSCard(grammar_exercise_id=exercise.id))

        await db.commit()
        print("Seed complete: 10-week roadmap + Week 1 vocab/grammar/SRS cards loaded.")


if __name__ == "__main__":
    asyncio.run(seed())
