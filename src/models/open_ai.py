import os

from dotenv import load_dotenv
import openai

from src.models.ai_service import AIService


class OpenAI(AIService):
    def query(self, ai_model: str, system_role_prompt: str, prompt: str) -> str | dict:

        try:
            load_dotenv()
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("API key is not set")

            openai.api_key = openai_api_key
            response = openai.chat.completions.create(
                model=ai_model,
                messages=[
                    {"role": "system", "content": system_role_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            # print(response.choices[0].message.content)
            return response.choices[0].message.content
        except Exception as e:
            print(f" Error querying OpenAI: {e}")
            return {"model_query_error": f"Query failed: {str(e)}"}
