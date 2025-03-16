from src.sampling.sampling_strategy import SamplingStrategy


class SamplesByFeature(SamplingStrategy):
    def sample(self, dataframe, feature, n: int):
        samples = dataframe.groupby(feature).head(n)
        return samples
