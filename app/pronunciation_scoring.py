"""Pronunciation clarity scoring -- a PROXY metric, not true phonetic
assessment.

Real phoneme-level pronunciation scoring (GOP scoring, formant analysis --
what Azure Pronunciation Assessment / ELSA / Speechace do) requires a
server-side ASR model with forced phoneme alignment and a paid API key.
That's out of scope for a two-person hobby app.

What IS feasible with zero extra cost: the browser's own Web Speech API
(SpeechRecognition) acts as an implicit judge. If you pronounce a word
clearly, the recognizer transcribes it correctly; if you mispronounce it,
its language model guesses wrong or produces a garbled result. Scoring the
similarity between the target text and what the browser heard is a
legitimate, widely-used proxy for clarity -- it just can't tell you *which*
phoneme was wrong, only that something was off.

Speech-to-text itself only ever happens client-side (SpeechRecognition is a
browser API; there's no server involvement in capturing/transcribing audio,
and critically no audio ever leaves the device to our backend). This module
only scores a transcript the browser already produced.
"""
from __future__ import annotations

import re
import unicodedata


def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")  # strip diacritics
    text = re.sub(r"[.,!?;:'\"]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _levenshtein(a: str, b: str) -> int:
    m, n = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m
    prev = list(range(n + 1))
    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
        prev = curr
    return prev[n]


def score_pronunciation(target: str, transcript: str) -> int:
    """Character-level similarity, 0-100. Robust to minor ASR mis-segmentation."""
    t = normalize_text(target)
    h = normalize_text(transcript)
    if not h:
        return 0
    dist = _levenshtein(t, h)
    max_len = max(len(t), len(h), 1)
    return max(0, round((1 - dist / max_len) * 100))


def word_diff(target: str, transcript: str) -> list[dict]:
    """Word-level LCS diff, for showing which words matched vs. were missed."""
    a = normalize_text(target).split()
    b = normalize_text(transcript).split()
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(dp[i - 1][j], dp[i][j - 1])

    matched = [False] * len(a)
    i, j = len(a), len(b)
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            matched[i - 1] = True
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return [{"word": word, "matched": matched[idx]} for idx, word in enumerate(a)]


def score_tier(score: int) -> dict:
    if score >= 85:
        return {"label": "Sangat jelas", "css_class": "tier-clear"}
    if score >= 60:
        return {"label": "Cukup jelas", "css_class": "tier-ok"}
    return {"label": "Coba lagi", "css_class": "tier-retry"}
