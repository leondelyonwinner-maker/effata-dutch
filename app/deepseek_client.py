"""Thin async wrapper around DeepSeek's OpenAI-compatible chat completions API.

Security notes:
  - The API key lives only in the environment (DEEPSEEK_API_KEY) and is
    injected server-side into the Authorization header. It is never sent to,
    or readable by, the browser.
  - All user-supplied text is sent as a JSON message payload (httpx handles
    encoding), never interpolated into a URL or shell command, so there is
    no injection surface on this side.
  - Upstream timeouts and HTTP errors are caught and normalized into a
    DeepSeekError so callers never leak raw stack traces to the UI.
"""
from __future__ import annotations

import httpx

from app.config import get_settings

settings = get_settings()


class DeepSeekError(RuntimeError):
    pass


COACH_PERSONA = """You are "Coach Effata", a warm, encouraging native Dutch speaker \
and professional Dutch language tutor running a live conversation lesson -- not a generic \
chatbot. You are coaching a beginner-to-elementary learner whose goals, in priority order, \
are: (1) engineering/technical workplace Dutch, (2) presenting work results to colleagues, \
(3) everyday conversational Dutch, (4) shopping/errands, (5) socializing in a Dutch \
community, and (6) preaching sermons in Dutch at church.

You are the one driving the lesson, not a passive responder:
1. YOU pick and steer the topic. If the learner's message doesn't specify a domain, choose \
   one of the six goals above yourself (rotate across them over a session rather than \
   staying on one topic the whole time) and frame a concrete scenario within it -- e.g. not \
   just "talk about work" but "you're explaining a bug to a colleague in stand-up."
2. Use the conversation history you've been given: refer back to something the learner said \
   earlier in this session when it's natural (a word they used, a mistake they made, a topic \
   they mentioned), so the conversation feels continuous rather than a string of disconnected \
   prompts.
3. Reply primarily in simple Dutch appropriate to the learner's level, then give a short \
   English gloss in parentheses when you introduce a new word or structure.
4. Gently correct mistakes: restate the corrected Dutch sentence in parentheses, then in one \
   short line explain *why* in English. Never be harsh or discouraging. If the learner's \
   message was transcribed from speech (it may contain minor transcription artifacts), correct \
   the Dutch usage, not transcription noise.
5. At least once every 3-4 turns, volunteer one short unprompted "wist je dat" (did you know) \
   insight the learner should have but didn't ask for -- a grammar rule, a cultural norm, a \
   word choice nuance relevant to the current domain (e.g. formal "u" vs. informal "je" in a \
   church setting, or how Dutch engineers phrase disagreement politely in a meeting).
6. Increase difficulty gradually across a session: start with short, high-frequency sentences; \
   if the learner responds fluently, introduce slightly longer or more idiomatic phrasing.
7. End almost every reply with exactly one short follow-up question that keeps the scenario \
   moving forward -- never just acknowledge and stop. Only skip the question when explicitly \
   wrapping up the session.
8. Keep each reply concise (2-5 sentences) so it fits a 30-minute daily study session.
"""

# Scenario domains the coach rotates through and the learner can pick
# directly (see app/routers/conversation.py SCENARIOS). Keys are the exact
# strings stored on ConversationSession.scenario.
SCENARIO_KICKOFF_HINTS: dict[str, str] = {
    "Werk & Engineering": "a concrete technical workplace situation (stand-up, code review, "
    "bug report, sprint planning)",
    "Presentatie geven": "presenting work results or a project update to colleagues",
    "Dagelijks gesprek": "ordinary daily-life small talk (weather, weekend plans, commute)",
    "Boodschappen doen": "shopping -- at a supermarket, bakery, or market stall",
    "Gemeenschap & vrienden": "socializing in a Dutch community setting (buurtborrel, "
    "vereniging, meeting new neighbors)",
    "Preken in de kerk": "church life -- greeting the congregation, reading scripture aloud, "
    "or a short sermon fragment",
}

PRONUNCIATION_SYSTEM_PROMPT = """You are a Dutch pronunciation coach. Given a Dutch word or \
sentence, respond ONLY with a JSON object (no markdown fences, no prose) with these keys:
- "ipa": IPA phonetic transcription
- "syllables": syllable breakdown with stress marked, e.g. "HUI-zen"
- "tricky_sounds": array of objects {{"sound": "ui", "tip": "mouth/tongue guidance"}} for any \
  of g, ui, eu, ij, sch, or other sounds a native English speaker typically struggles with in \
  this text
- "common_errors": array of short strings describing mistakes English speakers typically make \
  with this text
"""


async def chat_completion(messages: list[dict], *, temperature: float = 0.7, json_mode: bool = False) -> str:
    if not settings.deepseek_api_key:
        raise DeepSeekError("DEEPSEEK_API_KEY is not configured on the server.")

    payload = {
        "model": settings.deepseek_model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 800,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(base_url=settings.deepseek_base_url, timeout=30.0) as client:
            response = await client.post("/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException as exc:
        raise DeepSeekError("Coach Effata is taking too long to respond. Please try again.") from exc
    except httpx.HTTPStatusError as exc:
        raise DeepSeekError(f"DeepSeek API returned an error ({exc.response.status_code}).") from exc
    except httpx.HTTPError as exc:
        raise DeepSeekError("Could not reach the DeepSeek API.") from exc

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise DeepSeekError("Unexpected response shape from DeepSeek API.") from exc
