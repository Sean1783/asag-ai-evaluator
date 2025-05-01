import pandas as pd

from src.sampling.sampling_strategy import SamplingStrategy


class SamplesByFeature(SamplingStrategy):

    def __init__(self, feature: str, num_samples: int = 1):
        self.feature = feature
        self.num_samples = num_samples

    def set_feature(self, feature: str):
        self.feature = feature

    def set_num_samples(self, num_samples: int):
        self.num_samples = num_samples

    def sample(self, dataframe: pd.DataFrame):
        try:
            if self.feature not in dataframe.columns:
                raise KeyError(f"Feature '{self.feature}' not found.")
            samples = dataframe.groupby(self.feature).head(self.num_samples)
            return samples
        except KeyError as e:
            raise KeyError(f"Invalid feature name: {str(e)}")
        except Exception as e:
            raise ValueError(f"An error occurred while sampling: {str(e)}")
