from abc import ABC, abstractmethod

class SamplingStrategy(ABC):
    # @abstractmethod
    # def sample(self, df, feature: str, n: int):
    #     pass

    @abstractmethod
    def sample(self, df):
        pass