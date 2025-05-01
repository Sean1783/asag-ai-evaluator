from datasets import load_dataset

from src.dataset.dataset_interface import DatasetInterface


class MeyergerDataset(DatasetInterface):
    def __init__(self):
        self.dataset_name = None
        self.dataset = None
        self.dataframe = None

    def load_dataset(self, dataset_name: str):
        try:
            self.dataset = load_dataset(dataset_name)
            self.prep_dataset()
        except FileNotFoundError as e:
            print(f"Dataset '{dataset_name}' not found: {e}")
        except ValueError as e:
            print(f"Error loading dataset '{dataset_name}': {e}")
        except Exception as e:
            print(f"Unexpected error loading dataset '{dataset_name}': {e}")

    def prep_dataset(self):
        self.dataframe = self.dataset["train"].to_pandas()
        feature_name_list = self.dataframe.columns.tolist()
        self.dataframe = self.dataframe.dropna(subset=feature_name_list)

    def get_dataset(self):
        return self.dataset

    def get_dataframe(self):
        return self.dataframe

    def get_q_and_a_feature_names(self):
        return {
            "question": "question",
            "answer": "provided_answer",
            "reference_answer": "reference_answer"
        }
