import boto3
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from botocore.exceptions import ClientError
from src.custom_exception import CustomException
from src.logger import get_logger
from utils.common_function import read_yaml
from config.paths_config import *
from dotenv import load_dotenv


# Initialize the logger
logger = get_logger(__name__)
load_dotenv()

class DataIngestion:
    def __init__(self, config):
        self.config = config
        self.dynamodb_table_name = self.config["aws"]["dynamodb_table_name"]
        self.region_name = self.config["aws"]["region_name"]

        # Fetch credentials from environment variables
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise CustomException("AWS credentials are not set in environment variables or .env file")

        # Initialize the DynamoDB resource with explicit credentials
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )
        self.table = self.dynamodb.Table(self.dynamodb_table_name)

    def fetch_data_from_dynamodb(self):
        """
        Fetches all data from the DynamoDB table.
        """
        try:
            logger.info(f"Fetching data from DynamoDB table: {self.dynamodb_table_name}")
            all_items = []
            response = self.table.scan()

            # Append the initial batch of items
            all_items.extend(response.get('Items', []))

            # Check if there's more data to fetch
            while 'LastEvaluatedKey' in response:
                logger.info("Fetching next page of results...")
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                all_items.extend(response.get('Items', []))

            logger.info(f"Successfully fetched {len(all_items)} records from DynamoDB.")
            return all_items

        except ClientError as e:
            logger.error(f"Error fetching data from DynamoDB: {e}")
            raise CustomException("Failed to fetch data from DynamoDB", e)

    def split_and_save_data(self, data):
        """
        Splits the data into train and test datasets and saves them as CSV files.
        """
        try:
            logger.info("Splitting data into train and test datasets")

            if not data:
                raise CustomException("No data available to split into train and test datasets")

            # Convert data to a pandas DataFrame
            df = pd.DataFrame(data)

            # Split data into train and test
            train_ratio = self.config["data_ingestion"]["train_ratio"]
            train_df, test_df = train_test_split(df, test_size=(1 - train_ratio), random_state=42)

            if not os.path.exists(RAW_DATA_PATH):
                os.makedirs(RAW_DATA_PATH)


            # Save to CSV
            train_df.to_csv(TRAIN_DATA_PATH, index=False, encoding='utf-8')
            test_df.to_csv(TEST_DATA_PATH, index=False, encoding='utf-8')

            logger.info(f"Train data saved to {TRAIN_DATA_PATH}")
            logger.info(f"Test data saved to {TEST_DATA_PATH}")

        except Exception as e:
            logger.error(f"Error splitting or saving data: {e}")
            raise CustomException("Failed to split and save data", e)

    def run(self):
        """
        Orchestrates the entire data ingestion process.
        """
        try:
            logger.info("Starting data ingestion process")

            # Fetch data from DynamoDB
            data = self.fetch_data_from_dynamodb()

            # Split the data into train and test and save them
            self.split_and_save_data(data)

            logger.info("Data ingestion process completed successfully")

        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
        finally:
            logger.info("End of data ingestion process")


if __name__ == "__main__":
    # Create an instance of the DataIngestion class with the configuration and execute the run method
    data_ingestion = DataIngestion(read_yaml(CONFIG_YAML))
    data_ingestion.run()
