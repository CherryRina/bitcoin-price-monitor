"""
Bitcoin Price Monitor - Main Script
Handles both data collection and hourly processing
"""

from src.bitcoin_price_manager import BitcoinPriceManager
from src.email_manager import EmailManager
from src.bitcoin_graph_generator import BitcoinGraphGenerator
from src.json_handler import JsonHandler 
from src.logger import Logger
from dotenv import load_dotenv
import sched
import time
import os


load_dotenv()
FILE_PATH = os.path.join('data', 'bitcoin_prices.json')
GET_REQUEST_INTERVAL = 60
GRAPH_INTERVAL = 3600
EMAIL_INTERVAL = 3600

scheduler = sched.scheduler(time.time, time.sleep) 


def get_and_save_bitcoin_price(logger, json_loader):
    bitcoin_endpoint = os.getenv("BITCOIN_ENDPOINT")
    bitcoin_manager = BitcoinPriceManager(endpoint=bitcoin_endpoint, logger=logger, json_loader=json_loader)
    timestamp, bitcoin_price = bitcoin_manager.get_bitcoin_data()
    logger.debug(f"Current Bitcoin information: {timestamp} - {bitcoin_price}")
    bitcoin_manager.save_data_to_json(file_path=FILE_PATH, timestamp=timestamp, bitcoin_price=bitcoin_price)
    scheduler.enter(GET_REQUEST_INTERVAL, 1, get_and_save_bitcoin_price, kwargs={"logger": logger, "json_loader": json_loader})


def generate_graph(logger, json_loader):
    graph_generator = BitcoinGraphGenerator(json_loader=json_loader, logger=logger)
    graph_generator.generate_graph()
    scheduler.enter(GRAPH_INTERVAL, 1, generate_graph, kwargs={"logger": logger, "json_loader": json_loader})


def send_email(logger, json_loader):
    src_email = os.getenv("SRC_EMAIL")
    src_email_password = os.getenv("SRC_EMAIL_PASSWORD")
    dst_email = os.getenv("DST_EMAIL")
    email_sender = EmailManager(src_email=src_email, src_email_password=src_email_password, dst_email=dst_email,json_loader=json_loader, logger=logger)
    email_title = "Bitcoin Status"
    email_message = email_sender.parse_json_data_to_maximum_price()
    email_letter = email_sender.create_message(title=email_title, message=email_message)
    email_sender.send_email(email_letter=email_letter)
    scheduler.enter(EMAIL_INTERVAL, 1, generate_graph, kwargs={"logger": logger, "json_loader": json_loader})


def main():
    """ main function """
    logger = Logger().logger
    logger.info("Started running...")
    json_loader = JsonHandler(logger=logger, file_path=FILE_PATH)

    scheduler.enter(0, 1, get_and_save_bitcoin_price, kwargs={"logger": logger, "json_loader": json_loader})
    scheduler.enter(GRAPH_INTERVAL, 1, generate_graph, kwargs={"logger": logger, "json_loader": json_loader})
    scheduler.enter(EMAIL_INTERVAL, 2, send_email, kwargs={"logger": logger, "json_loader": json_loader})
    scheduler.run()

    
if __name__ == "__main__":
    main()
