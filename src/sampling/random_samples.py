import pandas as pd

from src.sampling.sampling_strategy import SamplingStrategy

class RandomSamples(SamplingStrategy):
    def __init__(self, num_samples: int=1):
        self.num_samples = num_samples

    def set_num_samples(self, num_samples : int):
        self.num_samples = num_samples

    def sample(self, dataframe : pd.DataFrame, feature : str=None, n : int=1) -> pd.DataFrame:
        return dataframe.sample(n=self.num_samples, random_state=30)