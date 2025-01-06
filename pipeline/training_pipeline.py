from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.model_training import ModelTraining
from config.paths_config import *
from utils.common_function import read_yaml


if __name__ == "__main__":
    
    data_ingestion = DataIngestion(read_yaml(CONFIG_YAML))
    data_ingestion.run()

    processor = DataProcessor(TRAIN_DATA_PATH, TEST_DATA_PATH, PROCESSED_DIR, CONFIG_YAML)
    processor.process()

    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    metrics = trainer.run()