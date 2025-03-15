from src.dataset.dataset_interface import DatasetInterface
from src.dataset.meyerger_dataset import MeyergerDataset


class DatasetFactory:
    @staticmethod
    def get_dataset(dataset_name : str):
        try:
            if dataset_name == "Meyerger/ASAG2024":
                myerger_dataset = MeyergerDataset()
                myerger_dataset.load_dataset(dataset_name)
                return myerger_dataset
        except ValueError:
            raise ValueError(f"Dataset {dataset_name} not found.")