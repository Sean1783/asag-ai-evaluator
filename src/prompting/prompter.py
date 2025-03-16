
class Prompter:
    _template = None

    @classmethod
    def load_template(cls, file_path="prompt_template.txt"):
        if cls._template is None:
            with open(file_path, "r") as file:
                cls._template = file.read()

    def __init__(self,
                 prompt_dataset_adapter,
                 full_system_role,
                 system_role,
                 system_role_adjective,
                 system_role_noun,
                 prompt_context,
                 grading_rubric):

        self.load_template()
        self.prompt_dataset_adapter = prompt_dataset_adapter
        self.full_system_role = full_system_role
        self.system_role = system_role
        self.system_role_adjective = system_role_adjective
        self.system_role_noun = system_role_noun
        self.prompt_context = prompt_context
        self.grading_rubric = grading_rubric

    def get_full_system_role_prompt(self):
        return self.full_system_role

    def get_system_role_adjective(self):
        return self.system_role_adjective

    def get_system_role_noun(self):
        return self.system_role_noun

    def get_system_role(self):
        return self.system_role

    def extract_question_and_answers(self, dataset_row):
        question = self.prompt_dataset_adapter.extract_question(dataset_row)
        student_answer = self.prompt_dataset_adapter.extract_answer(dataset_row)
        reference_answer = self.prompt_dataset_adapter.extract_reference_answer(dataset_row)
        return question, student_answer, reference_answer

    def generate_full_prompt(self, dataset_row):
        question, student_answer, reference_answer = self.extract_question_and_answers(dataset_row)
        return self._template.format(
            prompt_context=self.prompt_context,
            question=question,
            student_answer=student_answer,
            reference_answer=reference_answer,
            grading_rubric=self.grading_rubric,
        )

    class PrompterBuilder:
        def __init__(self):
            self.prompt_adapter = None
            self.full_system_role = ""
            self.system_role = ""
            self.system_role_noun = ""
            self.system_role_adjective = ""
            self.prompt_context = ""
            self.grading_rubric = ""

        def with_prompt_adapter(self, prompt_adapter):
            self.prompt_adapter = prompt_adapter
            return self

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
            return Prompter(self.prompt_adapter,
                            self.full_system_role,
                            self.system_role,
                            self.system_role_adjective,
                            self.system_role_noun,
                            self.prompt_context,
                            self.grading_rubric)
