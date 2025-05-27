from src.logger import Logger
import json

class JsonLoader():
    def __init__(self, logger, file_path):
        self.logger = logger
        self.json_data = self.safe_read_json(file_path)


    def list_json_data():
        pass


    def save_to_json_file():
        pass

    
    def json_empty(self, json_data):
        """
        Recieves JSON file
        Returns True if empty, flase if not
        """
        if not json_data:
            self.logger.warning("Json is empty")
            return True 
        return False


    def safe_read_json(self, file_path:str):
        """
        Recieves file path and loads its contents, has many error handling logs
        Returns the contents of the json as a dictionary (or empty one in failure)
        """
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.info(f"File '{file_path}' not found. Creating new one")
            with open(file_path, "w") as file:
                json.dump({}, file)  # default empty JSON object
        except json.JSONDecodeError:
            self.logger.info(f"File '{file_path}' is corrupted. Creating new one")
        except Exception as e:
            self.logger.info(f"Unexpected error loading '{file_path}': {e}. Creating new one")
        return {}
    

    def safe_write_to_json(self, file_path:str, new_json:dict):
        """ Safely load JSON file and return dict (or empty dict on failure) """
        try:
            with open(file_path, "w")  as file:
                json.dump(new_json, file, indent=4)
                return
        except FileNotFoundError:
            self.logger.info(f"File '{file_path}' not found. Creating new one")
        except json.JSONDecodeError:
            self.logger.info(f"File '{file_path}' is corrupted. Creating new one")
        except Exception as e:
            self.logger.info(f"Unexpected error loading '{file_path}': {e}. Creating new one")
        return {}
    # TODO: check the error handling