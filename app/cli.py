"""Operator CLI -- the only way users get created in this app (no public
signup form, see app/auth.py docstring).

Usage:
  python -m app.cli hash-passcode "your-passcode"
  python -m app.cli create-user <username> "<Display Name>" "<passcode>"
  python -m app.cli list-users
  python -m app.cli sync-srs-cards
"""
from __future__ import annotations

import asyncio
import sys

from sqlalchemy import select

from app.auth import hash_passcode, normalize_username
from app.db import AsyncSessionLocal, init_models
from app.models import GrammarExercise, SRSCard, User, VocabItem


async def _sync_srs_cards() -> int:
    """Idempotent: creates one SRSCard per (user, vocab item) and (user,
    grammar exercise) pair that doesn't already have one. Safe to re-run any
    time new curriculum content is seeded, or a new user is created."""
    async with AsyncSessionLocal() as db:
        users = (await db.execute(select(User))).scalars().all()
        vocab_ids = set((await db.execute(select(VocabItem.id))).scalars().all())
        exercise_ids = set((await db.execute(select(GrammarExercise.id))).scalars().all())

        created = 0
        for user in users:
            existing_vocab = set(
                (
                    await db.execute(
                        select(SRSCard.vocab_item_id).where(
                            SRSCard.user_id == user.id, SRSCard.vocab_item_id.is_not(None)
                        )
                    )
                )
                .scalars()
                .all()
            )
            existing_exercise = set(
                (
                    await db.execute(
                        select(SRSCard.grammar_exercise_id).where(
                            SRSCard.user_id == user.id, SRSCard.grammar_exercise_id.is_not(None)
                        )
                    )
                )
                .scalars()
                .all()
            )
            for vocab_id in vocab_ids - existing_vocab:
                db.add(SRSCard(user_id=user.id, vocab_item_id=vocab_id))
                created += 1
            for exercise_id in exercise_ids - existing_exercise:
                db.add(SRSCard(user_id=user.id, grammar_exercise_id=exercise_id))
                created += 1

        await db.commit()
        return created


async def _create_user(username: str, display_name: str, passcode: str) -> None:
    await init_models()
    username = normalize_username(username)

    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(User).where(User.username == username))
        if existing.scalars().first() is not None:
            print(f"User '{username}' already exists.", file=sys.stderr)
            raise SystemExit(1)

        db.add(User(username=username, display_name=display_name, passcode_hash=hash_passcode(passcode)))
        await db.commit()

    created = await _sync_srs_cards()
    print(f"Created user '{username}' ({display_name}) with {created} SRS cards.")


async def _list_users() -> None:
    async with AsyncSessionLocal() as db:
        users = (await db.execute(select(User).order_by(User.id))).scalars().all()
        if not users:
            print("No users yet. Create one with: python -m app.cli create-user <username> \"<Name>\" \"<passcode>\"")
            return
        for u in users:
            print(f"{u.id}\t{u.username}\t{u.display_name}\tcreated {u.created_at:%Y-%m-%d}")


def main() -> None:
    args = sys.argv[1:]

    if len(args) == 2 and args[0] == "hash-passcode":
        print(hash_passcode(args[1]))
        return

    if len(args) == 4 and args[0] == "create-user":
        asyncio.run(_create_user(args[1], args[2], args[3]))
        return

    if len(args) == 1 and args[0] == "list-users":
        asyncio.run(_list_users())
        return

    if len(args) == 1 and args[0] == "sync-srs-cards":
        created = asyncio.run(_sync_srs_cards())
        print(f"Synced SRS cards: {created} created.")
        return

    print(
        "Usage:\n"
        '  python -m app.cli hash-passcode "your-passcode"\n'
        '  python -m app.cli create-user <username> "<Display Name>" "<passcode>"\n'
        "  python -m app.cli list-users\n"
        "  python -m app.cli sync-srs-cards",
        file=sys.stderr,
    )
    raise SystemExit(1)


if __name__ == "__main__":
    main()
