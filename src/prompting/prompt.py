class Prompt:
    def __init__(
            self,
            dataset_row,
            full_system_role,
            system_role,
            system_role_adjective,
            system_role_noun,
            prompt_context,
            grading_rubric,
            output_format_instruction):
        self.full_system_role = full_system_role
        self.system_role = system_role
        self.system_role_adjective = system_role_adjective
        self.system_role_noun = system_role_noun
        self.prompt_context = prompt_context
        self.grading_rubric = grading_rubric
        self.output_format_instruction = (
            f"""Return the score as a **plain JSON object** with **no additional text or markdown formatting** in the following format:
            ```json
            {{"score": <your score here>, "reason": "<your brief explanation here>"}}
            {output_format_instruction}
        """)
        self.question, self.student_answer, self.reference_answer = self.extract_question_and_answers(dataset_row)

    def get_full_system_role_prompt(self):
        return self.full_system_role

    def get_system_role_adjective(self):
        return self.system_role_adjective

    def get_system_role_noun(self):
        return self.system_role_noun

    def get_system_role(self):
        return self.system_role

    @staticmethod
    def extract_question_and_answers(self, dataset_row):
        row_dict = dataset_row._asdict()
        question = row_dict["question"]
        student_answer = row_dict["provided_answer"]
        reference_answer = row_dict["reference_answer"]
        return question, student_answer, reference_answer

    def generate_full_prompt(self):
        reference_answer = None
        if self.reference_answer is not None:
            reference_answer = (
                f"""The following reference answer represents a perfect answer to the question.
        
Reference Answer: {self.reference_answer}""")

        full_prompt = f"""
{self.prompt_context}

Question: {self.question}

Student's Answer: {self.student_answer}

{reference_answer}

{self.grading_rubric}

{self.output_format_instruction}
"""
        return full_prompt

    class PromptBuilder:
        def __init__(self):
            self.full_system_role = ""
            self.system_role = ""
            self.system_role_noun = ""
            self.system_role_adjective = ""
            self.prompt_context = ""
            self.grading_rubric = ""
            self.output_format_instruction = ""

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

        def with_output_format_instruction(self, output_format_instruction):
            self.output_format_instruction = output_format_instruction
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
                          self.system_role_noun, self.prompt_context, self.grading_rubric,
                          self.output_format_instruction)
