from src.api_handler import ApiHandler
from datetime import datetime as dt

class BitcoinManager(ApiHandler):
    def __init__(self, endpoint, logger, json_loader):
        super().__init__(endpoint, logger)
        self.json_loader = json_loader
    

    def get_bitcoin_data(self) -> tuple[str, float]:
        """ 
        Does a get request to the bitcoin-data endpoint
        Returns current Bitcoins price and time
        """
        try:
            api_get_response = self.get_request()
            bitcoin_price = float(api_get_response["data"]["amount"])
            timestamp = dt.now().strftime('%H:%M:%S')
            return timestamp, bitcoin_price
        except Exception as e:
            self.logger.error("Failed to fetch Bitcoin price: {e}. Check the API response JSON file")
            exit(1)

    
    def save_data_to_json(self, file_path:str, timestamp:str, bitcoin_price:float) -> None:
        """ 
        Recieves path to file, timestamp and bitcoins price
        Saves them into the json file and loggs
        """
        new_json = self.json_loader.json_data
        new_json[timestamp] = bitcoin_price
        self.json_loader.safe_write_to_json(file_path=file_path, new_json=new_json)
        self.logger.info("Bitcoin data was added to json")