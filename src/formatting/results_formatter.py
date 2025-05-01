import json
from typing import Dict, Tuple, Any

from src.prompting.prompter import Prompter


def format_result5(dataset_row: Tuple[Any, ...], prompter: Prompter, ai_response: str, ai_model: str) -> Dict[Any, Any]:
    formatted_result = dict(dataset_row._asdict())
    formatted_result.update({
        "system_role_info": prompter.get_full_system_role_prompt(),
        "prompt_context": prompter.get_prompt_context(),
        "grading_rubric": prompter.get_grading_rubric(),
        "full_prompt": prompter.get_full_prompt(),
        "ai_model": ai_model,
    })
    try:
        formatted_result["ai_response"] = json.loads(ai_response)
    except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")
    return formatted_result
