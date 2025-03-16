import os

import anthropic
from dotenv import load_dotenv

from src.models.ai_service import AIService

class AnthropicAI(AIService):
    def query(self, ai_model : str, system_role_prompt : str | None,  prompt : str) -> str|None :

        try:
            load_dotenv()
            anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
            if not anthropic_api_key:
                raise ValueError("API key is not set")

            client = anthropic.Anthropic(api_key=anthropic_api_key)
            response = client.messages.create(
                model=ai_model,
                max_tokens=100,
                system=system_role_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f" Error querying Anthropic: {e}")