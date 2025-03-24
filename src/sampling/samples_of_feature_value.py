import pandas as pd

from src.sampling.sampling_strategy import SamplingStrategy

class SamplesOfFeatureValue(SamplingStrategy):
    def __init__(self, feature : str, feature_value : str, num_samples : int = 0):
        self.feature = feature
        self.feature_value = feature_value
        self.num_samples = num_samples

    def set_feature(self, feature: str):
        self.feature = feature

    def set_feature_value(self, feature_value: str):
        self.feature = feature_value

    def sample(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            if self.feature not in dataframe.columns:
                raise KeyError(f"Feature '{self.feature}' not found.")
            samples = dataframe[dataframe[self.feature] == self.feature_value]
            if samples.empty:
                raise ValueError("No records found for the given value.")
            else:
                if self.num_samples > 0:
                    samples = samples.head(self.num_samples)
                return samples
        except KeyError as e:
            raise KeyError(f"Invalid feature name: {str(e)}")
        except Exception as e:
            raise ValueError(f"An error occurred while sampling: {str(e)}")