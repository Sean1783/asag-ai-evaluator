from src.sampling.sampling_strategy import SamplingStrategy


class RandomSamples(SamplingStrategy):

    def sample(self, dataset, feature, n):
        return dataset.sample(n=n, random_state=100)