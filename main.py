"""
Bitcoin Price Monitor - Main Script
Handles both data collection and hourly processing
"""

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

    # generate graph
    graph_generator = GraphGenerator(json_loader=json_loader, logger=logger)
    graph_generator.generate_graph()

    # send email
    src_email = os.getenv("SRC_EMAIL")
    src_email_password = os.getenv("SRC_EMAIL_PASSWORD")
    dst_email = os.getenv("DST_EMAIL")

    email_sender = EmailSender(src_email=src_email, src_email_password=src_email_password, dst_email=dst_email,json_loader=json_loader, logger=logger)
    email_title = "Bitcoin Status"
    email_message = email_sender.find_max_price()
    email_letter = email_sender.create_message(title=email_title, message=email_message)
    email_sender.send_email(email_letter=email_letter)

    
if __name__ == "__main__":
    main()
