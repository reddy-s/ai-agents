import pandas as pd
import logging

logger = logging.getLogger(__name__)


class LocalStorage:

    @staticmethod
    def write(df: pd.DataFrame, path: str) -> bool:
        """
        Write a pandas DataFrame to a JSON file.

        This method takes a DataFrame and writes it to a JSON file at the specified path using the 'records' orientation
        and without including the index.

        Args:
            df (pd.DataFrame): The DataFrame to write to the JSON file.
            path (str): The file path where the JSON file will be saved.

        Returns:
            bool: True if the DataFrame is successfully written to the file, False otherwise.
        """
        try:
            df.to_json(path, orient="records", lines=True, index=False)
            return True
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def read(path: str) -> pd.DataFrame | None:
        """
        Read a CSV file into a pandas DataFrame.

        This method reads a CSV file from the specified path into a DataFrame. If there is an error during the read operation,
        it logs the error and returns None.

        Args:
            path (str): The file path from where the CSV file will be read.

        Returns:
            pd.DataFrame | None: The DataFrame if successfully read from the file, None otherwise.
        """
        try:
            df = pd.read_csv(path)
            return df
        except Exception as e:
            logger.error(e)
            return None
