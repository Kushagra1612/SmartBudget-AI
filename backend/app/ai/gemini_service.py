from google import genai
from google.genai import types

from app.config import settings
from app.ai.prompts import SYSTEM_PROMPT


class GeminiService:
    """
    Service responsible for communicating with the Gemini API.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_MODEL

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Send a prompt to Gemini and return the generated text.
        """

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