from typing import List

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
        return self.prompt.get_full_system_role_prompt()

    def query_ai(self, samples: pd.DataFrame, qa_feature_names: str, system_role: str) -> List[dict]:
        results = []
        print("Querying AI...")
        for row in samples.itertuples():
            full_prompt = self.prompt.generate_full_prompt(row, qa_feature_names)
            response = self.model.query(system_role, full_prompt)
            result = format_result5(row, self.prompt, response)
            results.append(result)
        return results

    def insert_results_into_database(self, results: List[dict]) -> None:
        print("Inserting results...")
        self.database.insert_documents(DbDetails.DATABASE_COLLECTION.value, results)

    def run(self):
        dataframe = self.generate_dataframe()
        samples = self.sampling_strategy.get_samples(dataframe, "", 2)
        qa_feature_names = self.generate_qa_feature_names()
        system_role = self.generate_system_role()
        results = self.query_ai(samples, qa_feature_names, system_role)
        self.insert_results_into_database(results)
        print("---Pipeline execution complete---")
