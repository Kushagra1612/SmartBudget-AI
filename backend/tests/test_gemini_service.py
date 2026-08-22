"""
Replaces the old manual test_gemini.py script.

Default `pytest` run: everything here is mocked -- no GEMINI_API_KEY
needed, no quota used, no network call, safe to run as often as you
like.

To also run the one real, live call against the actual Gemini API
(useful after changing the model name, prompt structure, or the
google-genai SDK version -- the kind of thing mocks can't catch):

    RUN_LIVE_GEMINI_TEST=1 pytest tests/test_gemini_service.py -v -s

That one needs a real GEMINI_API_KEY in your .env and will count against
your quota, which is exactly why it's opt-in instead of running every time.
"""

import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.ai.gemini_service import GeminiService


def _fake_client(response_text: str | None = "Mocked Gemini response."):
    fake_response = SimpleNamespace(text=response_text)
    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response
    return fake_client


def test_generate_returns_the_response_text():
    with patch("app.ai.gemini_service.genai.Client", return_value=_fake_client()):
        service = GeminiService()
        result = service.generate("Say hello.")

    assert result == "Mocked Gemini response."


def test_generate_strips_whitespace_from_the_response():
    with patch(
        "app.ai.gemini_service.genai.Client",
        return_value=_fake_client("  padded response  \n"),
    ):
        service = GeminiService()
        result = service.generate("Say hello.")

    assert result == "padded response"


def test_generate_handles_an_empty_response_gracefully():
    with patch(
        "app.ai.gemini_service.genai.Client", return_value=_fake_client(response_text="")
    ):
        service = GeminiService()
        result = service.generate("Say hello.")

    assert result == "No response generated."


def test_generate_gives_a_friendly_message_on_quota_exhaustion():
    fake_client = MagicMock()
    fake_client.models.generate_content.side_effect = Exception(
        "429 RESOURCE_EXHAUSTED: quota exceeded"
    )

    with patch("app.ai.gemini_service.genai.Client", return_value=fake_client):
        service = GeminiService()
        result = service.generate("Say hello.")

    assert "quota" in result.lower()
    assert "unavailable" in result.lower()


def test_generate_gives_a_generic_message_on_other_errors():
    fake_client = MagicMock()
    fake_client.models.generate_content.side_effect = Exception("connection reset")

    with patch("app.ai.gemini_service.genai.Client", return_value=fake_client):
        service = GeminiService()
        result = service.generate("Say hello.")

    assert "unable to generate" in result.lower()


@pytest.mark.skipif(
    os.environ.get("RUN_LIVE_GEMINI_TEST") != "1",
    reason="Live Gemini call -- opt in with RUN_LIVE_GEMINI_TEST=1 (uses real quota).",
)
def test_live_gemini_call_actually_works():
    """
    The one real integration check: sends an actual prompt to the actual
    API using your real GEMINI_API_KEY, and just confirms *something*
    sensible comes back. Not for every run -- for when you've changed
    something about how Gemini gets called and want to know it still
    works against the real service, not just the mocks.
    """

    service = GeminiService()
    result = service.generate("Reply with exactly the word: pong")

    assert isinstance(result, str)
    assert len(result) > 0
    assert "unable to generate" not in result.lower()
