from datetime import datetime as dt
import requests

class ApiHandler():
    def __init__(self, endpoint, logger):
        self.endpoint = endpoint
        self.logger = logger

    def check_valid_status_code(self, status_code):
        if status_code != 200:
            self.logger.error(f"API returned status code: {status_code}")
            return False
        return True


    def get_request(self):
        response = requests.get(url=self.endpoint)
        if self.check_valid_status_code(response.status_code):
            return response.json()
        
    
