from typing import Optional, Union
from datetime import datetime as dt
import json
import requests


class BitcoinPriceManager():
    def __init__(self, endpoint, logger, json_loader):
        self.endpoint = endpoint
        self.logger = logger
        self.json_loader = json_loader
    

    def get_bitcoin_data(self) -> tuple[str, float]:
        """ 
        Does a get request to the bitcoin-data endpoint
        Returns current Bitcoins price and time
        """
        timestamp = dt.now().strftime('%H:%M:%S')
        api_get_response = self._get_request()
        try:
            if api_get_response == None:
                self.logger.error(f"An error appeared while tring to make a GET request")
                return timestamp, 0
            bitcoin_price = float(api_get_response["data"]["amount"])
            return timestamp, bitcoin_price
        except Exception as e:
            self.logger.fatal(f"Failed to fetch Bitcoin price: {e}. Check the API response")
            exit(1)

    
    def save_data_to_json(self, file_path:str, timestamp:str, bitcoin_price:float) -> None:
        """ 
        Recieves path to file, timestamp and bitcoins price
        Saves them into the json file and loggs
        """
        new_json = self.json_loader.json_data
        new_json[timestamp] = bitcoin_price
        self.json_loader.safe_write_to_json(file_path=file_path, data=new_json)
        self.logger.info("Bitcoin data was added to json")


    def _get_request(self) -> Optional[Union[dict, list]]:
        """
        Helper method does an API request 
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