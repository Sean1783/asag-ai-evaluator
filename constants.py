from enum import Enum

class AIModels(Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    CHATGPT_4O_LATEST = "chatgpt-4o-latest"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    CLAUDE_3_5_HAIKU = "claude-3-5-haiku-20241022"
    GEMINI_2_FLASH = "gemini-2.0-flash"

class FeatureNameValues(Enum):
    QUESTION = "question"
    ANSWER = "answer"
    REFERENCE_ANSWER = "reference_answer"
    AI_SCORE = "score"

class SampleStrategyNames(Enum):
    RANDOM = "random"
    BY_FEATURE = "by_feature"

class DbDetails(Enum):
    DATABASE_NAME = "results_db_1"
    DATABASE_COLLECTION = "test_collection_1"