from abc import ABC, abstractmethod

class AIService(ABC):
    @abstractmethod
    def query(self, ai_model : str, system_role_prompt : str | None, prompt : str) -> str | None:
        pass