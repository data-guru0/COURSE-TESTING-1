import os


################## CONFIG ###########################

CONFIG_YAML = "config/config.yaml"

#################### DATA INGESTION ###############

RAW_DATA_PATH = "artifacts/raw"
TRAIN_DATA_PATH = os.path.join(RAW_DATA_PATH, "train.csv")
TEST_DATA_PATH = os.path.join(RAW_DATA_PATH, "test.csv")


##################### DATA PROCESSING #####################33

PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")


######################## MODEL TRAINING ############################

MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"