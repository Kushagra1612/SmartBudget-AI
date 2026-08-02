from app.ai.gemini_service import GeminiService

service = GeminiService()

response = service.generate(
    "Explain in one sentence why saving money is important."
)

print(response)