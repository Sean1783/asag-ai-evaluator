from src.prompting.prompt_dataset_adapter import DatasetAdapter

class MeyergerAdapter(DatasetAdapter):

    def extract_question(self, dataset_row):
        row_dict = dataset_row._asdict()
        question = row_dict["question"]
        return question

    def extract_answer(self, dataset_row):
        row_dict = dataset_row._asdict()
        student_answer = row_dict["provided_answer"]
        return student_answer

    def extract_reference_answer(self, dataset_row):
        row_dict = dataset_row._asdict()
        reference_answer = row_dict["reference_answer"]
        return reference_answer

