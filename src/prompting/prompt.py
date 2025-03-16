class Prompt:

    _template = None
    @classmethod
    def load_template(cls, file_path="prompt_template.txt"):
        if cls._template is None:
            with open(file_path, "r") as file:
                cls._template = file.read()

    def __init__(
            self,
            dataset_row,
            full_system_role,
            system_role,
            system_role_adjective,
            system_role_noun,
            prompt_context,
            grading_rubric,
    ):
        self.load_template()
        self.full_system_role = full_system_role
        self.system_role = system_role
        self.system_role_adjective = system_role_adjective
        self.system_role_noun = system_role_noun
        self.prompt_context = prompt_context
        self.grading_rubric = grading_rubric
        self.question, self.student_answer, self.reference_answer = self.extract_question_and_answers(dataset_row)

    def get_full_system_role_prompt(self):
        return self.full_system_role

    def get_system_role_adjective(self):
        return self.system_role_adjective

    def get_system_role_noun(self):
        return self.system_role_noun

    def get_system_role(self):
        return self.system_role

    def extract_question_and_answers(self, dataset_row):
        row_dict = dataset_row._asdict()
        question = row_dict["question"]
        student_answer = row_dict["provided_answer"]
        reference_answer = row_dict["reference_answer"]
        return question, student_answer, reference_answer

    def generate_full_prompt(self):
        reference_answer_text = f"\nReference Answer: {self.reference_answer}" if self.reference_answer else ""
        return self._template.format(
            prompt_context=self.prompt_context,
            question=self.question,
            student_answer=self.student_answer,
            reference_answer=reference_answer_text,
            grading_rubric=self.grading_rubric,
        )

    class PromptBuilder:
        def __init__(self):
            self.full_system_role = ""
            self.system_role = ""
            self.system_role_noun = ""
            self.system_role_adjective = ""
            self.prompt_context = ""
            self.grading_rubric = ""

        def with_prompt_context(self, prompt_context):
            self.prompt_context = prompt_context
            return self

        def with_system_role(self, system_role):
            self.system_role = system_role
            return self

        def with_system_role_adjective(self, system_role_adjective):
            self.system_role_adjective = system_role_adjective
            return self

        def with_system_role_noun(self, system_role_noun):
            self.system_role_noun = system_role_noun
            return self

        def with_grading_rubric(self, grading_rubric):
            self.grading_rubric = grading_rubric
            return self

        def set_full_system_role(self):
            if self.system_role != "" and self.system_role_noun != "":
                if self.system_role_adjective != "":
                    self.full_system_role = self.system_role + " " + self.system_role_adjective + " " + self.system_role_noun
                else:
                    self.full_system_role = self.system_role + " " + self.system_role_noun

        def build(self, dataset_row):
            self.set_full_system_role()
            return Prompt(dataset_row, self.full_system_role, self.system_role, self.system_role_adjective,
                          self.system_role_noun, self.prompt_context, self.grading_rubric)
