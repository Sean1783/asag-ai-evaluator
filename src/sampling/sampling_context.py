from src.sampling.sampling_strategy import SamplingStrategy

class SamplingContext:
    def __init__(self, sampling_strategy: SamplingStrategy):
        self.sampling_strategy = sampling_strategy

    def set_sampling_strategy(self, sampling_strategy):
        self.sampling_strategy = sampling_strategy

    def get_samples(self, dataset, feature: str, n: int):
        if self.sampling_strategy is None:
            raise RuntimeError("Sampling strategy is not set")
        return self.sampling_strategy.sample(dataset, feature, n)

