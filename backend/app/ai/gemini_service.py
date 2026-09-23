from google import genai
from google.genai import types

from app.config import settings
from app.ai.prompts import SYSTEM_PROMPT


class GeminiService:
    """
    Service responsible for communicating with the Gemini API.

    Fallback chain:
      1. Primary model (GEMINI_MODEL env var, default: gemini-3.5-flash-lite)
      2. On quota exhausted (429) -> gemini-2.5-flash-lite
      3. On model retired (404)   -> gemini-3.6-flash
    """

    QUOTA_FALLBACK_MODEL = "gemini-2.5-flash-lite"
    RETIRED_FALLBACK_MODEL = "gemini-3.6-flash"

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL or "gemini-3.6-flash"
        self.client = None

        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Error initializing Gemini client: {e}")

    def _call_model(self, model: str, prompt: str) -> str:
        """Helper to call a specific model and return text."""
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
            ),
        )
        return response.text.strip() if response.text else "No response generated."

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the generated text.
        Falls back to gemini-2.5-flash-lite if quota is exhausted,
        and to gemini-3.6-flash if the primary model is retired.
        """
        if not self.client or not self.api_key:
            return (
                "Warning: Gemini API key is missing or not configured on the server. "
                "Please configure GEMINI_API_KEY in your server environment variables."
            )

        try:
            return self._call_model(self.model, prompt)

        except Exception as e:
            print("=" * 60)
            print("GEMINI ERROR")
            print(type(e).__name__)
            print(e)
            print("=" * 60)

            error_message = str(e)

            # Quota exhausted -> fallback to gemini-2.5-flash-lite
            if (
                "RESOURCE_EXHAUSTED" in error_message
                or "429" in error_message
                or "quota" in error_message.lower()
            ):
                print(
                    f"Quota exhausted on '{self.model}'. "
                    f"Retrying with fallback: {self.QUOTA_FALLBACK_MODEL}"
                )
                try:
                    return self._call_model(self.QUOTA_FALLBACK_MODEL, prompt)
                except Exception as quota_fallback_err:
                    print(f"Quota fallback model also failed: {quota_fallback_err}")
                    return (
                        "Warning: AI service is temporarily unavailable - "
                        "quota exceeded on all models. Please try again later."
                    )

            # Model retired / not found -> fallback to gemini-3.6-flash
            if (
                "NOT_FOUND" in error_message
                or "404" in error_message
                or "no longer available" in error_message
            ) and self.model != self.RETIRED_FALLBACK_MODEL:
                print(
                    f"Model '{self.model}' retired. "
                    f"Retrying with: {self.RETIRED_FALLBACK_MODEL}"
                )
                try:
                    return self._call_model(self.RETIRED_FALLBACK_MODEL, prompt)
                except Exception as retired_fallback_err:
                    print(f"Retired fallback model failed: {retired_fallback_err}")

            return (
                "Warning: Unable to generate AI response at the moment. "
                "Please check your GEMINI_API_KEY and GEMINI_MODEL configuration."
            )
