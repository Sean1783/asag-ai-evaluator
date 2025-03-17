from constants import FeatureNameValues

class Prompter:
    _template = None

    @classmethod
    def load_template(cls, file_path="prompt_template2.txt"):
        if cls._template is None:
            with open(file_path, "r") as file:
                cls._template = file.read()

    def __init__(self,
                 full_system_role,
                 system_role,
                 system_role_adjective,
                 system_role_noun,
                 prompt_context,
                 grading_rubric):

        self.load_template()
        self.full_system_role = full_system_role
        self.system_role = system_role
        self.system_role_adjective = system_role_adjective
        self.system_role_noun = system_role_noun
        self.prompt_context = prompt_context
        self.grading_rubric = grading_rubric
        self.full_prompt = None

    def get_full_system_role_prompt(self):
        return self.full_system_role

    def get_system_role_adjective(self):
        return self.system_role_adjective

    def get_system_role_noun(self):
        return self.system_role_noun

    def get_system_role(self):
        return self.system_role

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
        # return self._template.format(
        #     prompt_context=self.prompt_context,
        #     question=question,
        #     answer=answer,
        #     reference_answer=reference_answer,
        #     grading_rubric=self.grading_rubric,
        # )
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
            self.full_system_role = ""
            self.system_role = ""
            self.system_role_noun = ""
            self.system_role_adjective = ""
            self.prompt_context = ""
            self.grading_rubric = ""

        def set_full_system_role(self):
            if self.system_role != "" and self.system_role_noun != "":
                if self.system_role_adjective != "":
                    self.full_system_role = self.system_role + " " + self.system_role_adjective + " " + self.system_role_noun
                else:
                    self.full_system_role = self.system_role + " " + self.system_role_noun

        def with_system_role(self, system_role):
            self.system_role = system_role
            return self

        def with_system_role_noun(self, system_role_noun):
            self.system_role_noun = system_role_noun
            return self

        def with_system_role_adjective(self, system_role_adjective):
            self.system_role_adjective = system_role_adjective
            return self

        def with_prompt_context(self, prompt_context):
            self.prompt_context = prompt_context
            return self

        def with_grading_rubric(self, grading_rubric):
            self.grading_rubric = grading_rubric
            return self

        def build(self):
            self.set_full_system_role()
            return Prompter(self.full_system_role,
                            self.system_role,
                            self.system_role_adjective,
                            self.system_role_noun,
                            self.prompt_context,
                            self.grading_rubric)
