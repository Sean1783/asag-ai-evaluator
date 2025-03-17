from src.database.database_manager import DatabaseManager
from src.dataset.dataset_factory import DatasetFactory
from src.pipeline.pipeline import Pipeline
from src.prompting.prompter import Prompter
from src.sampling.random_samples import RandomSamples
from src.sampling.samples_by_feature import SamplesByFeature
from src.sampling.sampling_context import SamplingContext
from src.test_runner.test_runner import *
from constants import AIModels, SampleStrategyNames

doc_source_file = "results/gpt-4o-mini_results_2025-02-23 10:12:13.json"

def dataset_tests():
    meyerger = DatasetFactory.get_dataset("Meyerger/ASAG2024")
    meyerger.prep_dataset()
    ds = meyerger.get_dataset()
    print(len(ds))

def sampling_tests():
    meyerger = DatasetFactory.get_dataset("Meyerger/ASAG2024")
    meyerger.prep_dataset()
    ds = meyerger.get_dataset()
    strategy = SamplingContext(RandomSamples())
    samples = strategy.get_samples(ds, "", 10)
    print(samples)
    strategy.set_sampling_strategy(SamplesByFeature())
    samples = strategy.get_samples(ds, "data_source", 5)
    print(samples)

def pipeline_tests():
    meyerger = DatasetFactory.get_dataset("Meyerger/ASAG2024")
    meyerger.prep_dataset()
    ds = meyerger.get_dataset()
    # strategy = SamplingContext(SamplesByFeature())
    strategy = SamplingContext(RandomSamples())
    # samples = strategy.get_samples(ds, "data_source", 1)
    samples = strategy.get_samples(ds, "", 5)
    ai_model = AIModels.GEMINI_2_FLASH.value
    ai_service = ModelContext(ai_model)
    test_results = run_test(samples, ai_service)
    save_results(f"results/{ai_model}_results", test_results)

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

def construct_prompter():
    meyerger = DatasetFactory.get_dataset("Meyerger/ASAG2024")
    meyerger.prep_dataset()
    ds = meyerger.get_dataset()
    strategy = SamplingContext(RandomSamples())
    samples = strategy.get_samples(ds, "", 2)
    qa_feature_names = meyerger.get_q_and_a_feature_names()
    prompt = (Prompter.PrompterBuilder()
              .with_system_role("You are a")
              .with_system_role_adjective("capable")
              .with_system_role_noun("genius")
              .build())

    for row in samples.itertuples(False):
        print(prompt.generate_full_prompt(row, qa_feature_names))

def pipeline_tester():
    pipeline = Pipeline()
    dataset = DatasetFactory.get_dataset("Meyerger/ASAG2024")
    dataframe = dataset.get_dataframe()
    # pipeline.set_dataset("Meyerger/ASAG2024")
    sampling_strategy = SamplingContext(RandomSamples())
    # pipeline.set_sampling_strategy(SampleStrategyNames.RANDOM)
    prompt = (Prompter.PrompterBuilder()
              .with_system_role("You are a")
              .with_system_role_adjective("capable")
              .with_system_role_noun("genius")
              .build())
    # pipeline.set_prompt()
    samples = sampling_strategy.get_samples(dataframe, "", 2)
    # pipeline.select_samples("", 2)
    ai_model = ModelContext(AIModels.GEMINI_2_FLASH.value)
    # pipeline.set_model(AIModels.GEMINI_2_FLASH)
    # pipeline.query_ai()

def pipeliner():
    dataset = DatasetFactory.get_dataset("Meyerger/ASAG2024")
    sampling_strategy = SamplingContext(RandomSamples())
    prompt = (Prompter.PrompterBuilder()
              .with_system_role("You are a")
              .with_system_role_adjective("capable")
              .with_system_role_noun("genius")
              .build())
    ai_model = ModelContext(AIModels.GEMINI_2_FLASH.value)
    pipeline = Pipeline(dataset, sampling_strategy, ai_model, prompt)
    pipeline.run()

def main():
    pipeliner()
    # pipeline_tester()
    # construct_prompter()
    # pipeline_tests()
    # sampling_tests()
    # dataset_tests()
    # get_documents_from_database()
    # insert_document()
    # insert_documents_into_database()
    # run_tests()
    # construct_prompt()


if __name__ == '__main__':
    main()