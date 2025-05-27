from src.bitcoin_manager import BitcoinManager
from src.email_sender import EmailSender
from src.graph_generator import GraphGenerator
from src.json_loader import JsonLoader
from src.logger import Logger

from dotenv import load_dotenv
import os



def main():
    """ main function """
    load_dotenv() 
    bitcoin_endpoint = os.getenv("BITCOIN_ENDPOINT")
    file_path = os.path.join('data', 'bitcoin_prices.json')

    # logger setup
    logger = Logger().logger
    logger.info("Started running...")

    # json loader setup
    json_loader = JsonLoader(logger=logger, file_path=file_path)

    # look for bitcoin price and save it
    bitcoin_manager = BitcoinManager(endpoint=bitcoin_endpoint, logger=logger, json_loader=json_loader)
    timestamp, bitcoin_price = bitcoin_manager.get_bitcoin_data()
    logger.debug(f"Current Bitcoin information: {timestamp} - {bitcoin_price}")
    bitcoin_manager.save_data_to_json(file_path=file_path, timestamp=timestamp, bitcoin_price=bitcoin_price)

    



    
    



if __name__ == "__main__":
    main()
