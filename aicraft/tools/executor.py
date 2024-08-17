import os
from streamlit.delta_generator import DeltaGenerator
from aicraft.types import CodingAgentResponse, Roles
import pandas as pd
import psycopg2
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SQLExecutor:
    db_params = {
        "dbname": "agents",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": "5432",
    }

    @staticmethod
    def execute(sql: str) -> pd.DataFrame:
        # Create a connection to the PostgreSQL database
        try:
            connection = psycopg2.connect(**SQLExecutor.db_params)
            df = pd.read_sql_query(sql, connection)
            return df

        except Exception as e:
            logger.error(e)
            return None
        finally:
            if connection is not None:
                connection.close()
