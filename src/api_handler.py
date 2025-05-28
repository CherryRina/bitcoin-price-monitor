import json
import requests
from typing import Optional, Union


class ApiHandler():
    def __init__(self, endpoint, logger):
        self.endpoint = endpoint
        self.logger = logger


    def get_request(self) -> Optional[Union[dict, list]]:
        """
        Method does an API request 
        Returns response as a dictionarry json, unless an error accured
        """
        try:
            response = requests.get(url=self.endpoint)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            self.logger.error("Request timed out")
            return None
        
        except requests.exceptions.ConnectionError:
            self.logger.error("Connection failed")
            return None
        
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            return None
        
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON response")
            return None
        
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None
        