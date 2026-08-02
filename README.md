# Effata Dutch

Personal Dutch language coach — FastAPI + server-rendered HTMX frontend + DeepSeek API, deployed on Render behind a single-user passcode gate. Installs as a home-screen PWA on iOS 26+ Safari/Chrome.

## Architecture

- **Backend:** FastAPI (async), SQLAlchemy 2.0 async ORM
- **DB:** Postgres in production (Render managed DB), SQLite for local dev
- **Frontend:** Jinja2 server-rendered templates + HTMX for partial updates, no build step
- **AI:** DeepSeek `chat/completions` (OpenAI-compatible), called server-side only
- **Auth:** single-user bcrypt-hashed passcode, signed session cookie, CSRF double-submit tokens, per-IP login rate limiting
- **Spaced repetition:** SM-2 algorithm (`app/srs.py`)

## Six coaching modules -> code map

| Module | Where |
|---|---|
| Personalized Fluency Plan | `app/seed_data.py` (`CURRICULUM`), rendered at `/` |
| Core Vocabulary Accelerator | `app/routers/vocabulary.py`, `/vocabulary` |
| Grammar Simplifier | `app/routers/grammar.py`, `/grammar` |
| Conversation Simulator | `app/routers/conversation.py`, `/conversation` (DeepSeek) |
| Pronunciation Coach | `app/routers/pronunciation.py`, `/pronunciation` (DeepSeek, JSON mode) |
| Memory Lock System | `app/routers/memory.py`, `/memory` (SM-2 review queue) |

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Generate your passcode hash and paste it into .env as APP_PASSCODE_HASH
python -m app.cli hash-passcode "your-passcode"

# Generate a session secret and paste it into .env as SESSION_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(48))"

# Add your DeepSeek key to .env as DEEPSEEK_API_KEY

python -m app.seed          # loads the 10-week roadmap + Week 1 content
uvicorn app.main:app --reload
```

Visit `http://localhost:8000`.

## Deploying (GitHub + Render, same pattern as Garmin Health)

1. Push this repo to GitHub.
2. In Render: **New -> Blueprint**, point it at the repo. `render.yaml` provisions the web service and a managed Postgres database together.
3. Set the two `sync: false` env vars manually in the Render dashboard (never commit these):
   - `APP_PASSCODE_HASH` — output of `python -m app.cli hash-passcode "..."`
   - `DEEPSEEK_API_KEY`
4. Deploy. `preDeployCommand` runs `python -m app.seed` automatically and is idempotent, so subsequent deploys won't duplicate content.
5. On iOS: open the Render URL in Safari or Chrome -> Share -> "Add to Home Screen" for the full-screen PWA experience.

## Known gap: home-screen icon

`app/static/icons/icon.svg` is the source icon. iOS wants rasterized PNGs for `apple-touch-icon`, which this repo does not generate automatically (kept `cairosvg` out of production dependencies on purpose — see `scripts/generate_icons.py`). Run that script once locally and commit the resulting `icon-180.png` / `icon-192.png` / `icon-512.png` before you care about the home-screen icon looking right; the app functions fully without it.

## Extending the curriculum

Weeks 2-10 are seeded as roadmap entries only (title/goal/module focus, no content yet). Add their vocab and grammar content to `app/seed_data.py` in the same shape as `WEEK_1_VOCAB_THEMES` / `WEEK_1_GRAMMAR_TOPICS`, wire them into `seed.py` the way Week 1 is wired, and rerun the seed (or let the next deploy's `preDeployCommand` pick it up — it only skips seeding if `CurriculumWeek` rows already exist, so for incremental content you'll want to seed additively rather than relying on the idempotency guard; see the comment in `app/seed.py`).
