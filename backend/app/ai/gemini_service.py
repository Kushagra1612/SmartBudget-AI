from google import genai
from google.genai import types

from app.config import settings
from app.ai.prompts import SYSTEM_PROMPT


class GeminiService:
    """
    Service responsible for communicating with the Gemini API.
    """

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL or "gemini-3.6-flash"
        self.client = None

        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Error initializing Gemini client: {e}")

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Gemini and return the generated text.
        """
        if not self.client or not self.api_key:
            return (
                "⚠️ Gemini API key is missing or not configured on the server. "
                "Please configure GEMINI_API_KEY in your server environment variables."
            )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3,
                ),
            )

            if response.text:
                return response.text.strip()

            return "No response generated."

        except Exception as e:
            print("=" * 60)
            print("GEMINI ERROR")
            print(type(e).__name__)
            print(e)
            print("=" * 60)

            error_message = str(e)

            # Auto-fallback if the specified model is retired or not found on the server
            if (
                "NOT_FOUND" in error_message
                or "404" in error_message
                or "no longer available" in error_message
            ) and self.model != "gemini-3.6-flash":
                try:
                    print("Retrying with fallback model: gemini-3.6-flash")
                    fallback_response = self.client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.3,
                        ),
                    )
                    if fallback_response.text:
                        return fallback_response.text.strip()
                except Exception as fallback_err:
                    print(f"Fallback model failed: {fallback_err}")

            if (
                "RESOURCE_EXHAUSTED" in error_message
                or "429" in error_message
                or "quota" in error_message.lower()
            ):
                return (
                    "⚠️ AI service is temporarily unavailable because the "
                    "Gemini API quota has been exceeded. "
                    "Please try again in a few minutes."
                )

            return (
                "⚠️ Unable to generate AI response at the moment. "
                "Please check your GEMINI_API_KEY and GEMINI_MODEL configuration."
            )