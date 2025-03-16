from src.dataset.dataset_factory import DatasetFactory
from constants import SampleStrategyNames, AIModels
from src.models.model_context import ModelContext
from src.sampling.random_samples import RandomSamples
from src.sampling.samples_by_feature import SamplesByFeature
from src.sampling.sampling_context import SamplingContext

class Pipeline:

    def __init__(self):
        self.dataset = None
        self.sampling_strategy_context = None
        self.model_context = None  # AI model interface
        self.db = None  # Database interface

    def set_dataset(self, dataset_name : str):
        ds_factory = DatasetFactory()
        dataset = ds_factory.get_dataset(dataset_name)
        self.dataset = dataset.prep_dataset()

    def set_sampling_strategy(self, sample_strategy : SampleStrategyNames):
        if sample_strategy == SampleStrategyNames.RANDOM:
            self.sampling_strategy_context = SamplingContext(RandomSamples())
        elif sample_strategy == SampleStrategyNames.BY_FEATURE:
            self.sampling_strategy_context = SamplingContext(SamplesByFeature())

    def set_model(self, model : AIModels):
        self.model_context = ModelContext(model.value)



