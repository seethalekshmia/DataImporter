import psycopg2
from psycopg2.extras import Json
from data_importer.logger import configure_logger

# Initialize logger
logger = configure_logger(__name__)

class Database:
    def __init__(self, db_config):
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS public.phone (
            phoneid TEXT PRIMARY KEY,
            phone_name TEXT,
            phone_data JSONB
        );
        """
        self.cursor.execute(query)
        self.connection.commit()

    def insert_data(self, phone_id, phone_name, phone_data):
        query = """
        INSERT INTO public.phone (phoneid, phone_name, phone_data)
        VALUES (%s, %s, %s)
        ON CONFLICT (phoneid) DO NOTHING;
        """
        self.cursor.execute(query, (phone_id, phone_name, Json(phone_data)))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
