# Graph Report - .  (2026-08-02)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 157 nodes · 363 edges · 13 communities (11 shown, 2 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.64)
- Token cost: 751 input · 1,236 output

## Graph Freshness
- Built from commit: `c1413249`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Database Models & Schema
- Project Setup & CLI
- Passcode Authentication
- Conversation & AI Chat
- Entrypoint & Dashboard
- Spaced Repetition System
- UI Templates
- Config & Grammar
- Icon Generation
- Exercise Result Partial

## God Nodes (most connected - your core abstractions)
1. `Base` - 15 edges
2. `Python Dependencies (requirements.txt)` - 14 edges
3. `Effata Dutch README` - 13 edges
4. `generate_csrf_token()` - 12 edges
5. `verify_csrf()` - 12 edges
6. `get_settings()` - 12 edges
7. `SRSCard` - 12 edges
8. `CurriculumWeek` - 10 edges
9. `require_login()` - 9 edges
10. `get_db()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Effata Dutch README` --references--> `Effata Dutch App Icon (icon.svg)`  [EXTRACTED]
  README.md → app/static/icons/icon.svg
- `Effata Dutch README` --references--> `itsdangerous 2.2.0`  [INFERRED]
  README.md → requirements.txt
- `Effata Dutch README` --references--> `bcrypt 4.0.1`  [EXTRACTED]
  README.md → requirements.txt
- `Effata Dutch README` --references--> `FastAPI 0.115.6`  [EXTRACTED]
  README.md → requirements.txt
- `Effata Dutch README` --references--> `Jinja2 3.1.5`  [EXTRACTED]
  README.md → requirements.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Jinja2 Page Templates Extending base.html** — app_templates_base, app_templates_conversation, app_templates_dashboard, app_templates_grammar, app_templates_login, app_templates_memory, app_templates_pronunciation, app_templates_vocabulary [EXTRACTED 0.95]

## Communities (13 total, 2 thin omitted)

### Community 0 - "Database Models & Schema"
Cohesion: 0.17
Nodes (20): Base, init_models(), Async SQLAlchemy engine/session plumbing., Create tables if they don't exist. Adequate for a single-tenant app;     swap fo, ConversationDifficulty, CurriculumWeek, GrammarExercise, GrammarTopic (+12 more)

### Community 1 - "Project Setup & CLI"
Cohesion: 0.12
Nodes (23): hash_passcode(), main(), Operator CLI: `python -m app.cli hash-passcode "your-passcode"`.  Prints a bcryp, Effata Dutch App Icon (icon.svg), DeepSeek Chat Completions API, PostgreSQL, Effata Dutch README, Render Blueprint (effata-dutch) (+15 more)

### Community 2 - "Passcode Authentication"
Cohesion: 0.17
Nodes (20): client_ip(), create_session_token(), is_authenticated(), is_ip_locked_out(), AsyncSession, Request, Single-user passcode authentication.  Threat model: this app has exactly one leg, read_session_token() (+12 more)

### Community 3 - "Conversation & AI Chat"
Cohesion: 0.24
Nodes (15): generate_csrf_token(), chat_completion(), DeepSeekError, Thin async wrapper around DeepSeek's OpenAI-compatible chat completions API.  Se, ConversationMessage, ConversationSession, conversation_page(), _get_or_create_session() (+7 more)

### Community 4 - "Entrypoint & Dashboard"
Cohesion: 0.16
Nodes (13): _assert_production_secrets_configured(), lifespan(), Request, Effata Dutch -- application entrypoint.  Run locally:     uvicorn app.main:app -, Fail fast on boot rather than silently signing session cookies with a     known/, redirect_unauthenticated(), security_headers(), dashboard() (+5 more)

### Community 5 - "Spaced Repetition System"
Cohesion: 0.28
Nodes (13): One spaced-repetition card, linked to either a vocab item or a grammar     exerc, ReviewLog, SRSCard, _utcnow(), _card_context(), _due_card(), grade_card(), AsyncSession (+5 more)

### Community 6 - "UI Templates"
Cohesion: 0.13
Nodes (15): Home-Screen Icon (icon-180.png), Base Layout Template (base.html), Conversation Simulator Template, Roadmap Dashboard Template, Grammar Simplifier Template, Login Template, Memory Lock Review Template, Single Chat Message Partial (+7 more)

### Community 7 - "Config & Grammar"
Cohesion: 0.21
Nodes (9): get_settings(), Centralized, typed application configuration.  All secrets are pulled exclusivel, Settings, check_exercise(), grammar_index(), AsyncSession, Request, Single shared Jinja2Templates instance so custom filters/globals are registered (+1 more)

## Knowledge Gaps
- **15 isolated node(s):** `Effata Dutch App Icon (icon.svg)`, `Roadmap Dashboard Template`, `Grammar Simplifier Template`, `Login Template`, `Vocabulary Accelerator Template` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Effata Dutch README` connect `Project Setup & CLI` to `UI Templates`?**
  _High betweenness centrality (0.351) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Base` (e.g. with `ConversationDifficulty` and `ConversationMessage`) actually correct?**
  _`Base` has 12 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Effata Dutch App Icon (icon.svg)`, `Roadmap Dashboard Template`, `Grammar Simplifier Template` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project Setup & CLI` be split into smaller, more focused modules?**
  _Cohesion score 0.11956521739130435 - nodes in this community are weakly interconnected._
- **Should `UI Templates` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._