import json
from typing import Dict, List, Tuple, Any

from src.prompting.prompt import Prompt

def format_result3(dataset_row : Tuple[Any, ...], prompt : Prompt, ai_response : str) -> Dict[Any, Any]:
    formatted_result = dict(dataset_row._asdict())
    system_role_info = {
        "system_role_prompt": prompt.get_full_system_role_prompt(),
        "system_role": prompt.get_system_role(),
        "system_role_adjective": prompt.get_system_role_adjective(),
        "system_role_noun": prompt.get_system_role_noun(),
    }
    formatted_result.update({
        "system_role_info": system_role_info,
        "full_prompt" : prompt.generate_full_prompt()
    })
    try:
        formatted_result["ai_response"] = json.loads(ai_response)
    except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")
    return formatted_result

def format_result2(
        dataset_row : Tuple[Any, ...],
        system_role : str,
        system_role_adjective: str,
        system_role_noun: str,
        system_role_prompt: str,
        full_prompt: str,
        ai_response
    ) -> Dict[Any, Any]:
    formatted_result = dict(dataset_row._asdict())
    formatted_result.update({
        "system_role_prompt": system_role_prompt,
        "system_role" : system_role,
        "system_role_adjective": system_role_adjective,
        "system_role_noun": system_role_noun,
        "full_prompt": full_prompt
    })
    try:
        formatted_result["ai_response"] = json.loads(ai_response)
    except json.decoder.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response: {e}")
    return formatted_result

def format_results(
        question : str,
        student_answer : str,
        reference_answer : str,
        student_grade : float,
        normalized_grade : float,
        system_role_temperament : str,
        system_role_prompt : str,
        full_prompt : str,
        ai_response : Dict):

    formatted_result = {"question": question,
                        "provided_answer": student_answer,
                        "reference_answer": reference_answer,
                        "grade": student_grade,
                        "normalized_grade": normalized_grade,
                        "temperament": system_role_temperament,
                        "system_role_prompt": system_role_prompt,
                        "prompt": full_prompt,
                        "response": ai_response}
    return formatted_result
