import pandas as pd

from src.sampling.sampling_strategy import SamplingStrategy


class RandomSamples(SamplingStrategy):

    def sample(self, dataframe : pd.DataFrame, feature, n):
        return dataframe.sample(n=n, random_state=100)