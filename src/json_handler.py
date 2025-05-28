import json
import os

class JsonHandler():
    def __init__(self, logger, file_path):
        self.logger = logger
        self.json_data = self.safe_read_json(file_path)


    def safe_read_json(self, file_path: str) -> dict:
        """
        Receives file path and loads its contents with comprehensive error handling.
        Returns the contents of the json as a dictionary (or empty one on failure).
        Creates the file with empty dict if it doesn't exist.
        """
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                self.logger.debug(f"Successfully loaded '{file_path}'")
                return data
        except FileNotFoundError:
            self.logger.warning(f"File '{file_path}' not found. Creating new one")
            return self._create_empty_json(file_path)
        except json.JSONDecodeError as e:
            self.logger.error(f"File '{file_path}' contains invalid JSON: {e}. Creating new one")
            return self._create_empty_json(file_path)
        except PermissionError:
            self.logger.error(f"Permission denied reading '{file_path}'")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error loading '{file_path}': {e}")
            return {}


    def _create_empty_json(self, file_path: str) -> dict:
        """
        Helper method to create an empty JSON file with error handling
        """
        try:
            with open(file_path, "w") as file:
                json.dump({}, file, indent=2)
            self.logger.info(f"Created new empty JSON file: '{file_path}'")
            return {}
        except PermissionError:
            self.logger.error(f"Permission denied creating '{file_path}'")
            return {}
        except Exception as e:
            self.logger.error(f"Failed to create '{file_path}': {e}")
            return {}
    

    def safe_write_to_json(self, file_path: str, data: dict) -> bool:
        """
        Safely write dictionary to JSON file with error handling.
        Returns True if successful, False otherwise.
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            self.logger.debug(f"Successfully wrote to '{file_path}'")
            return True
        except PermissionError:
            self.logger.error(f"Permission denied writing to '{file_path}'")
            return False
        except OSError as e:
            self.logger.error(f"OS error writing to '{file_path}': {e}")
            return False
        except TypeError as e:
            self.logger.error(f"Data not JSON serializable for '{file_path}': {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error writing to '{file_path}': {e}")
            return False