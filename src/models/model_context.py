from src.models.anthropic_ai import AnthropicAI
from src.models.gemini_ai import GeminiAI
from src.models.open_ai import OpenAI
from constants import AIModels

class ModelContext:
    MODEL_MAP = {
        "gpt-4o-mini": OpenAI,
        "chatgpt-4o-latest": OpenAI,
        "claude-3-haiku-20240307": AnthropicAI,
        "claude-3-5-haiku-20241022": AnthropicAI,
        "gemini-2.0-flash": GeminiAI,
    }

    def __init__(self, ai_model):
        self.ai_service = None
        self.ai_model = None
        self.set_ai_model(ai_model)

    def set_ai_model(self, ai_model : AIModels) -> None:
        service = self.MODEL_MAP.get(ai_model.value)
        if service is None:
            raise ValueError(f"Unknown AI model: {ai_model.value}")
        else:
            self.ai_service = service()
            self.ai_model = ai_model.value


    # def set_ai_model(self, ai_model : str) -> None:
    #     service = self.MODEL_MAP.get(ai_model)
    #     if service is None:
    #         raise ValueError(f"Unknown AI model: {ai_model}")
    #     else:
    #         self.ai_service = service()
    #         self.ai_model = ai_model

    def query(self, system_role_prompt : str,  prompt : str) -> str|None:
        return self.ai_service.query(self.ai_model, system_role_prompt, prompt)
