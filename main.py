from src.database.database_manager import DatabaseManager
from src.dataset.dataset_factory import DatasetFactory
from src.pipeline.pipeline import Pipeline
from src.sampling.random_samples import RandomSamples
from src.sampling.samples_of_feature_value import SamplesOfFeatureValue
from src.sampling.sampling_context import SamplingContext
from src.prompting.prompter import Prompter
from src.models.model_context import ModelContext
from constants import AIModels, DbDetails

def execute_pipeline():
    dataset = DatasetFactory.get_dataset("Meyerger/ASAG2024")
    ds_feature = "data_source"
    collection_feature_name = DbDetails.DB_COLLECTION_BEETLE.value
    num_samples = 300
    sampling_strategy = SamplingContext(SamplesOfFeatureValue(ds_feature, collection_feature_name, num_samples))
    prompt = (Prompter.PrompterBuilder()
              .with_grading_rubric("Provide a score from 0.0 to 1.0")
              .with_system_role("You are talented grader")
              .build())
    ai_model_name = AIModels.GPT_4O_MINI.value
    ai_model = ModelContext(ai_model_name)
    db_manager = DatabaseManager(DbDetails.MYERGER_DB_NAME.value)
    db_manager.set_collection(collection_feature_name)
    pipeline = Pipeline(dataset, sampling_strategy, ai_model, prompt, db_manager)
    pipeline.run()

def main():
    execute_pipeline()


if __name__ == '__main__':
    main()