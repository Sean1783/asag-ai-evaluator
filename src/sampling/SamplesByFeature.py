from src.sampling.SamplingStrategy import SamplingStrategy


class SamplesByFeature(SamplingStrategy):
    def sample(self, dataframe, feature, n: int):
        # sample_list = []
        samples = dataframe.groupby(feature).head(n)
        # sample_list.append(samples)
        # return sample_list
        return samples
