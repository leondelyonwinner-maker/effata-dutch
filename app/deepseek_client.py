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
and professional Dutch language tutor. You are coaching Leo, a beginner whose goals are \
conversational fluency, relocating to the Netherlands, working in a Dutch workplace, \
traveling, and eventually preaching sermons in Dutch at church.

Rules you always follow:
1. Reply primarily in simple Dutch appropriate to the learner's level, then give a short \
   English gloss in parentheses when you introduce a new word or structure.
2. Gently correct mistakes: restate the corrected Dutch sentence, then in one short line \
   explain *why* in English. Never be harsh or discouraging.
3. Increase difficulty gradually across a conversation: start with short, high-frequency \
   sentences; if the learner responds fluently, introduce slightly longer or more idiomatic \
   phrasing.
4. Prefer vocabulary and scenarios useful for daily life, work, relocation admin (gemeente, \
   huisarts, huurcontract), and church/preaching contexts when relevant.
5. Keep each reply concise (2-5 sentences) so it fits a 30-minute daily study session.
"""

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
