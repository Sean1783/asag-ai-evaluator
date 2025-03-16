from abc import ABC, abstractmethod

class DatasetAdapter(ABC):
    @abstractmethod
    def extract_question(self, row):
        pass

    @abstractmethod
    def extract_answer(self, row):
        pass

    @abstractmethod
    def extract_reference_answer(self, row):
        pass

