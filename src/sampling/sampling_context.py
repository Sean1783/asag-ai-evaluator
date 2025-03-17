import pandas as pd

from src.sampling.sampling_strategy import SamplingStrategy

class SamplingContext:
    def __init__(self, sampling_strategy: SamplingStrategy=None):
        self.sampling_strategy = sampling_strategy

    def set_sampling_strategy(self, sampling_strategy : SamplingStrategy):
        self.sampling_strategy = sampling_strategy

    def get_samples(self, dataframe : pd.DataFrame, feature: str=None, n: int=1) -> pd.DataFrame:
        if self.sampling_strategy is None:
            raise RuntimeError("Sampling strategy is not set")
        return self.sampling_strategy.sample(dataframe, feature, n)

