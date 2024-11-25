import logging
import os
import yaml
from data_importer.api_client import APIClient
from data_importer.db import Database
from data_importer.logger import configure_logger

# Configure logger
logger = configure_logger()

def load_config():
    # Get the absolute path of the project directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the config.yaml file
    config_path = os.path.join(base_dir, "config/config.yaml")  # Correct relative path
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def main():
    try:
        # Load configuration
        config = load_config()

        # Initialize API client
        api_url = config["api"]["url"]
        api_client = APIClient(api_url)

        # Fetch data from API
        logger.info("Fetching data from the API...")
        data = api_client.fetch_data()

        if not data:
            logger.warning("No data retrieved from the API.")
            return
        logger.info(f"Fetched {len(data)} records from the API.")

        # Initialize database connection
        db_config = config["database"]
        database = Database(db_config)
        database.connect()

        # Insert data into the database
        logger.info("Inserting data into the database...")
        for record in data:
            phone_id = record["id"]
            phone_name = record.get("name", None)
            phone_data = record.get("data", {})
            database.insert_data(phone_id, phone_name, phone_data)
        logger.info("Data insertion complete.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Execution complete.")

if __name__ == "__main__":
    main()
