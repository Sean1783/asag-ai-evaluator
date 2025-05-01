from typing import Tuple, Any


def system_role_formatter(temperament: str) -> str:
    system_role_prompt = f"You are a/an {temperament} grader."
    return system_role_prompt


def prompt_formatter2(dataset_row: Tuple[Any, ...]) -> str:
    row_dict = dataset_row._asdict()
    question = row_dict["question"]
    student_answer = row_dict["provided_answer"]
    reference_answer = row_dict["reference_answer"]

    full_prompt = f"""
    Evaluate the student's answer to the following question. 

    Question: {question}

    Student's Answer: {student_answer}

    The following reference answer represents a perfect answer to the question.

    Reference Answer: {reference_answer}

    ### **Grading Criteria:**
    - Assign a numerical grade from 0.0 to 1.0, where:
      - 0.0 = Completely incorrect
      - 1.0 = Perfect answer
    - A score of 0.1 would represent almost no correctness. 
    - A score of 0.2 would represent very little correctness. 
    - A score of 0.8 would represent substantial correctness.
    - A score of 0.9 would represent almost perfect correctness.
    - Return the score as a **plain JSON object** with **no additional text or markdown formatting** in the following format:
      ```json
      {{"score": <your score here>, "reason": "<your brief explanation here>"}}
    - Do not include any backticks or other markdown delimiters. Just return the JSON object.
    """
    return full_prompt


def prompt_formatter(question: str, student_answer: str, reference_answer: str) -> str:
    full_prompt = f"""
    Evaluate the student's answer to the following question. 

    Question: {question}

    Student's Answer: {student_answer}

    The following reference answer represents a perfect answer to the question.
     
    Reference Answer: {reference_answer}

    ### **Grading Criteria:**
    - Assign a numerical grade from 0.0 to 1.0, where:
      - 0.0 = Completely incorrect
      - 1.0 = Perfect answer
    - A score of 0.1 would represent almost no correctness. 
    - A score of 0.2 would represent very little correctness. 
    - A score of 0.8 would represent substantial correctness.
    - A score of 0.9 would represent almost perfect correctness.
    - Return the score as a **plain JSON object** with **no additional text or markdown formatting** in the following format:
      ```json
      {{"score": <your score here>, "reason": "<your brief explanation here>"}}
    - Do not include any backticks or other markdown delimiters. Just return the JSON object.
    """
    return full_prompt
