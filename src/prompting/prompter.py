from constants import FeatureNameValues


class Prompter:
    _template = None

    @classmethod
    def load_template(cls, file_path="prompt_template2.txt"):
        if cls._template is None:
            with open(file_path, "r") as file:
                cls._template = file.read()

    def __init__(self,
                 system_role,
                 prompt_context,
                 grading_rubric):
        self.load_template()
        self.system_role = system_role
        self.prompt_context = prompt_context
        self.grading_rubric = grading_rubric
        self.full_prompt = None

    def get_full_system_role_prompt(self):
        return self.system_role

    # def get_system_role(self):
    #     return self.system_role

    def get_prompt_context(self):
        return self.prompt_context

    def get_grading_rubric(self):
        return self.grading_rubric

    def extract_question_and_answers(self, dataset_row, qa_feature_names):
        row_dict = dataset_row._asdict()
        q_string = qa_feature_names[FeatureNameValues.QUESTION.value]
        a_string = qa_feature_names[FeatureNameValues.ANSWER.value]
        ref_a_string = qa_feature_names[FeatureNameValues.REFERENCE_ANSWER.value]
        question = row_dict[q_string]
        answer = row_dict[a_string]
        reference_answer = row_dict[ref_a_string]
        return question, answer, reference_answer

    def generate_full_prompt(self, dataset_row, qa_feature_names):
        question, answer, reference_answer = self.extract_question_and_answers(dataset_row, qa_feature_names)
        self.full_prompt = self._template.format(
            prompt_context=self.prompt_context,
            question=question,
            answer=answer,
            reference_answer=reference_answer,
            grading_rubric=self.grading_rubric,
        )
        return self.full_prompt

    def get_full_prompt(self):
        return self.full_prompt

    class PrompterBuilder:
        def __init__(self):
            self.system_role = ""
            self.prompt_context = ""
            self.grading_rubric = ""

        def with_system_role(self, system_role):
            self.system_role = system_role
            return self

        def with_prompt_context(self, prompt_context):
            self.prompt_context = prompt_context
            return self

        def with_grading_rubric(self, grading_rubric):
            self.grading_rubric = grading_rubric
            return self

        def build(self):
            return Prompter(self.system_role,
                            self.prompt_context,
                            self.grading_rubric)