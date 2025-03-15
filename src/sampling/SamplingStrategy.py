from abc import ABC, abstractmethod

class SamplingStrategy(ABC):
    @abstractmethod
    def sample(self, df, feature: str, n: int):
        pass