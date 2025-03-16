from datasets import load_dataset

from src.dataset.dataset_interface import DatasetInterface

class MeyergerDataset(DatasetInterface):
    def __init__(self):
        self.dataset_name = None
        self.dataset = None

    def load_dataset(self, dataset_name : str):
        try:
            self.dataset = load_dataset(dataset_name)
        except FileNotFoundError as e:
            print(f"Dataset '{dataset_name}' not found: {e}")
        except ValueError as e:
            print(f"Error loading dataset '{dataset_name}': {e}")
        except Exception as e:
            print(f"Unexpected error loading dataset '{dataset_name}': {e}")

    def prep_dataset(self):
        self.dataset = self.dataset["train"].to_pandas()
        feature_name_list = self.dataset.columns.tolist()
        self.dataset = self.dataset.dropna(subset=feature_name_list)

    def get_dataset(self):
        return self.dataset

