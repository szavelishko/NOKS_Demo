"""Обращение к модели Gemini.

Правила (см. replit.md):
- ключ берётся ТОЛЬКО из переменной окружения GEMINI_API_KEY (раздел Secrets в Replit);
- модель задаётся переменной GEMINI_MODEL, по умолчанию DEFAULT_MODEL;
- модель получает готовые цифры (JSON), посчитанные кодом, и пишет только текст.
"""
import json
import os

from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-flash-latest"


def model_name() -> str:
    return os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)


def key_is_set() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))


def _client() -> genai.Client:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "Не найден GEMINI_API_KEY. Откройте Tools → Secrets и добавьте ключ."
        )
    return genai.Client(api_key=key)


def ask_gemini(prompt: str, system: str | None = None, temperature: float = 0.2) -> str:
    """Текстовый ответ модели. При ошибке возвращает строку, начинающуюся с «Ошибка:»."""
    try:
        resp = _client().models.generate_content(
            model=model_name(),
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system, temperature=temperature
            ),
        )
        return resp.text or ""
    except Exception as e:  # noqa: BLE001
        return f"Ошибка: {e}"


def ask_gemini_json(prompt: str, system: str | None = None, temperature: float = 0.1):
    """Ответ модели в формате JSON (dict или list). При ошибке — {'error': '...'}."""
    try:
        resp = _client().models.generate_content(
            model=model_name(),
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                response_mime_type="application/json",
            ),
        )
        return json.loads(resp.text)
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}
