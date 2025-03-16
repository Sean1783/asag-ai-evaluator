from abc import ABC, abstractmethod

class DatasetInterface(ABC):

    @abstractmethod
    def load_dataset(self, dataset_name : str):
        pass

    @abstractmethod
    def prep_dataset(self):
        pass

    @abstractmethod
    def get_q_and_a_feature_names(self):
        pass
