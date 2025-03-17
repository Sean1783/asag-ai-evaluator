from typing import List
import json

from constants import DbDetails
from src.database.database_manager import DatabaseManager
from src.dataset.dataset_interface import DatasetInterface
from src.formatting.results_formatter import format_result5
from src.models.model_context import ModelContext
from src.prompting.prompter import Prompter
from src.sampling.sampling_context import SamplingContext

import pandas as pd


class Pipeline:
    def __init__(self,
                 dataset: DatasetInterface,
                 sampling_strategy: SamplingContext,
                 model: ModelContext,
                 prompt: Prompter,
                 database: DatabaseManager = None):

        self.dataset = dataset
        self.sampling_strategy = sampling_strategy
        self.model = model
        self.prompt = prompt
        self.database = database

    def generate_dataframe(self) -> pd.DataFrame:
        print("Generating dataframe...")
        return self.dataset.get_dataframe()

    def generate_samples(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        print("Generating samples...")
        return self.sampling_strategy.get_samples(dataframe, "", 2)

    def generate_qa_feature_names(self) -> str:
        print("Generating q&a feature names...")
        return self.dataset.get_q_and_a_feature_names()

    def generate_system_role(self) -> str:
        print("Generating full system role...")
        # return self.prompt.get_full_system_role_prompt()
        return self.prompt.get_system_role()

    # def generate_full_system_role(self) -> str:
    #     print("Generating full system role...")
    #     return self.prompt.get_full_system_role_prompt()

    def query_ai(self, samples: pd.DataFrame, qa_feature_names: str, system_role: str) -> List[dict]:
        results = []
        print("Querying AI...")
        for row in samples.itertuples():
            full_prompt = self.prompt.generate_full_prompt(row, qa_feature_names)
            response = self.model.query(system_role, full_prompt)
            result = format_result5(row, self.prompt, response)
            results.append(result)
        # for result in results:
            # json_formatted_str = json.dumps(result, indent=2)
            # print(json_formatted_str)
            # print(result)

        return results

    def insert_results_into_database(self, results: List[dict]) -> None:
        print("Inserting results...")
        self.database.insert_documents(DbDetails.DATABASE_COLLECTION.value, results)

    def run(self):
        dataframe = self.generate_dataframe()
        samples = self.sampling_strategy.get_samples(dataframe, "", 2)
        qa_feature_names = self.generate_qa_feature_names()
        # system_role = self.generate_full_system_role()
        system_role = self.generate_system_role()
        results = self.query_ai(samples, qa_feature_names, system_role)
        self.insert_results_into_database(results)
        # print("---Pipeline execution complete---")
        # results = []
        # for row in samples.itertuples():
        #     full_prompt = self.prompt.generate_full_prompt(row, qa_feature_names)
        #     response = self.model.query(system_role, full_prompt)
        #     result = format_result5(row, self.prompt, response)
        #     results.append(result)
        # for result in results:
        #     print(result)
        # print("---Pipeline execution complete---")

    #
    # def __init__(self):
    #     self.dataset = None
    #     # self.dataframe = None
    #     self.sampling_strategy_context = None
    #     self.model_context = None  # AI model interface
    #     self.prompter = None # Contains prompt preamble and system role
    #     self.samples = None # The Dataset samples that will be fed to AI
    #     self.db = None  # Database interface

    #
    #
    # def set_dataset(self, dataset_name : str):
    #     self.dataset = DatasetFactory().get_dataset(dataset_name)
    #     self.dataset.prep_dataset()
    #     # self.dataframe = dataset.get_dataset()
    #
    # def set_sampling_strategy(self, sample_strategy : SampleStrategyNames):
    #     if sample_strategy == SampleStrategyNames.RANDOM:
    #         self.sampling_strategy_context = SamplingContext(RandomSamples())
    #     elif sample_strategy == SampleStrategyNames.BY_FEATURE:
    #         self.sampling_strategy_context = SamplingContext(SamplesByFeature())
    #
    # def set_model(self, model : AIModels):
    #     self.model_context = ModelContext(model.value)
    #
    # def set_prompt(self):
    #     self.prompter = (Prompter.PrompterBuilder()
    #                 .with_system_role("You are a")
    #                 .with_system_role_adjective("talented")
    #                 .with_system_role_noun("engineer")
    #                 .build())
    #
    # def select_samples(self, feature : str, num_samples : int):
    #     dataframe = self.dataset.get_dataframe()
    #     self.samples = self.sampling_strategy_context.get_samples(dataframe, feature, num_samples)
    #
    # def query_ai(self):
    #     results_data = []
    #     qa_feature_names = self.dataset.get_q_and_a_feature_names()
    #     system_role = self.prompter.get_full_system_role_prompt()
    #     for row in self.samples.itertuples():
    #         full_prompt = self.prompter.generate_full_prompt(row, qa_feature_names)
    #         response = self.model_context.query(system_role, full_prompt)
    #         print(full_prompt)
    #         print(response)
    #
