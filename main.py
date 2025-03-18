from src.database.database_manager import DatabaseManager
from src.dataset.dataset_factory import DatasetFactory
from src.pipeline.pipeline import Pipeline
from src.sampling.random_samples import RandomSamples
from src.sampling.sampling_context import SamplingContext
from src.prompting.prompter import Prompter
from src.models.model_context import ModelContext
from constants import AIModels, DbDetails

def execute_pipeline():
    dataset = DatasetFactory.get_dataset("Meyerger/ASAG2024")
    sampling_strategy = SamplingContext(RandomSamples(100))
    prompt = (Prompter.PrompterBuilder()
              .with_grading_rubric("Provide a score from 0.0 to 1.0")
              .with_system_role("You are talented professor")
              .build())
    ai_model = ModelContext(AIModels.GPT_4O_MINI.value)
    db_manager = DatabaseManager(DbDetails.DATABASE_NAME.value)
    pipeline = Pipeline(dataset, sampling_strategy, ai_model, prompt, db_manager)
    pipeline.run()

def main():
    execute_pipeline()


if __name__ == '__main__':
    main()