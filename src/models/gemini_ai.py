import os

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

from src.models.ai_service import AIService

class GeminiAI(AIService):
    def query(self, ai_model : str, system_role_prompt : str | None, prompt : str) -> str | None:
        try:
            load_dotenv()
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if not gemini_api_key:
                raise ValueError("API key is not set")
            client = genai.Client(api_key=gemini_api_key)
            GenerateContentConfig()
            response = client.models.generate_content(
                model=ai_model,
                contents=prompt,
                config=GenerateContentConfig(system_instruction=system_role_prompt, response_mime_type="application/json")
            )
            return response.text
        except Exception as e:
            print(f"Error querying Gemini: {e}")