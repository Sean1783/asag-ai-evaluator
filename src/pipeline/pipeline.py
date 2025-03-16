from src.dataset.dataset_factory import DatasetFactory
from constants import SampleStrategyNames, AIModels
from src.dataset.dataset_interface import DatasetInterface
from src.formatting.results_formatter import format_result4
from src.models.model_context import ModelContext
from src.prompting.prompter import Prompter
from src.sampling.random_samples import RandomSamples
from src.sampling.samples_by_feature import SamplesByFeature
from src.sampling.sampling_context import SamplingContext

class Pipeline:
    def __init__(self,
                 dataset : DatasetInterface,
                 sampling_strategy : SamplingContext,
                 model : ModelContext):
        self.dataset = dataset
        self.sampling_strategy = sampling_strategy
        self.model = model




    def __init__(self):
        self.dataset = None
        # self.dataframe = None
        self.sampling_strategy_context = None
        self.model_context = None  # AI model interface
        self.prompter = None # Contains prompt preamble and system role
        self.samples = None # The Dataset samples that will be fed to AI
        self.db = None  # Database interface




    def set_dataset(self, dataset_name : str):
        self.dataset = DatasetFactory().get_dataset(dataset_name)
        self.dataset.prep_dataset()
        # self.dataframe = dataset.get_dataset()

    def set_sampling_strategy(self, sample_strategy : SampleStrategyNames):
        if sample_strategy == SampleStrategyNames.RANDOM:
            self.sampling_strategy_context = SamplingContext(RandomSamples())
        elif sample_strategy == SampleStrategyNames.BY_FEATURE:
            self.sampling_strategy_context = SamplingContext(SamplesByFeature())

    def set_model(self, model : AIModels):
        self.model_context = ModelContext(model.value)

    def set_prompt(self):
        self.prompter = (Prompter.PrompterBuilder()
                    .with_system_role("You are a")
                    .with_system_role_adjective("talented")
                    .with_system_role_noun("engineer")
                    .build())

    def select_samples(self, feature : str, num_samples : int):
        dataframe = self.dataset.get_dataframe()
        self.samples = self.sampling_strategy_context.get_samples(dataframe, feature, num_samples)

    def query_ai(self):
        results_data = []
        qa_feature_names = self.dataset.get_q_and_a_feature_names()
        system_role = self.prompter.get_full_system_role_prompt()
        for row in self.samples.itertuples():
            full_prompt = self.prompter.generate_full_prompt(row, qa_feature_names)
            response = self.model_context.query(system_role, full_prompt)
            print(full_prompt)
            print(response)

