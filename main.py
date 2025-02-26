from src.database.database_manager import DatabaseManager
from src.test_runner.test_runner import *
from constants import *

doc_source_file = "results/gpt-4o-mini_results_2025-02-23 10:12:13.json"

def run_tests() -> None:
    samples = select_data(1200, 1215)
    ai_model = AIModels.GEMINI_2_FLASH.value
    ai_service = ModelContext(ai_model)
    test_results = run_test(samples, ai_service)
    save_results(f"results/{ai_model}_results", test_results)
    print("Run tests complete")

def insert_document_into_database() -> None:
    db_manager = DatabaseManager("test_database")
    with open(doc_source_file, "r") as file:
        data = json.load(file)
    result_id = db_manager.insert_document("test_collection", data[0])
    print(f"Result ID: {result_id}")

def insert_documents_into_database() -> None:
    db_manager = DatabaseManager("test_database")
    with open(doc_source_file, "r") as file:
        data = json.load(file)
    inserted_ids = db_manager.insert_documents("test_collection", data)
    for id_num in inserted_ids:
        print(id_num)

def get_documents_from_database() -> None:
    db_manager = DatabaseManager("test_database")
    results = db_manager.find_documents("test_collection")
    for result in results:
        print(result)

def construct_prompt():
    samples = select_data(0, 1)
    for row in samples.itertuples(False):
        prompt = (Prompt.PromptBuilder()
                  .with_system_role("You are a")
                  .with_system_role_adjective("capable")
                  .with_system_role_noun("genius")
                  .with_prompt_context("Evaluate the student's answer to the following question.")
                  .with_grading_rubric("A score of 1.00 is a perfect score and a score of 0.00 is a horrible score.")
                  .build(row))
        print(prompt.generate_full_prompt())

def main():
    # get_documents_from_database()
    # insert_document()
    # insert_documents_into_database()
    run_tests()
    # construct_prompt()

if __name__ == '__main__':
    main()