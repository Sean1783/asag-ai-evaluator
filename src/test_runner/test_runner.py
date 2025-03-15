import datetime

from datasets import load_dataset
import pandas as pd

from src.models.model_context import ModelContext
from src.formatting.prompt_formatter import *
from src.formatting.results_formatter import *
from src.prompting.prompt import Prompt

def select_data(start : int, end : int) -> pd.DataFrame:
    ds = load_dataset("Meyerger/ASAG2024")
    df = ds["train"].to_pandas()
    data_samples = df.iloc[start:end]
    return data_samples

def run_test(samples : pd.DataFrame, ai_model_context : ModelContext) -> List[Dict[Any, Any]]:
    results_data = []
    prompt_builder = (Prompt.PromptBuilder()
              .with_system_role("You are an")
              .with_system_role_adjective("intelligent")
              .with_system_role_noun("grader")
              .with_prompt_context(
f"""Evaluate the student's answer to the following question and assign it a number grade in the range of 0.00 to 1.00.""")
              .with_grading_rubric(
f"""Use the below examples as a grading reference:
- A score of 1.00 is a completely correct answer.
- A score of 0.00 is a completely incorrect answer.
- A score of 0.90 would be for an answer that is almost completely correct.
- A score of 0.10 would be for an answer that is almost completely incorrect."""))

    for row in samples.itertuples(False):
        # print(row)
        prompt = prompt_builder.build(row)
        full_prompt = prompt.generate_full_prompt()
        # print(full_prompt)
        system_role_prompt = prompt.get_full_system_role_prompt()
        response = ai_model_context.query(system_role_prompt, full_prompt)
        formatted_result = format_result3(row, prompt, response)
        results_data.append(formatted_result)
    return results_data

def save_results(file_name, results_data : List[Dict]) -> None:
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d_%H:%M:%S")
    full_file_name = file_name + "_" + formatted_time + ".json"
    with open(full_file_name, "w") as results_file:
        json.dump(results_data, results_file, indent=4)