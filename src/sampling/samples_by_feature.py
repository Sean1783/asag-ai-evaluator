import pandas as pd

from src.sampling.sampling_strategy import SamplingStrategy

class SamplesByFeature(SamplingStrategy):
    def sample(self, dataframe : pd.DataFrame, feature : str, n: int):
        try:
            if feature not in dataframe.columns:
                raise KeyError(f"Feature '{feature}' not found.")
            samples = dataframe.groupby(feature).head(n)
            return samples
        except KeyError as e:
            raise KeyError(f"Invalid feature name: {str(e)}")
        except Exception as e:
            raise ValueError(f"An error occurred while sampling: {str(e)}")