import logging
import os

class Logger():
    def __init__(self):
        self.logger = self.setup_logger()


    def setup_logger(self):
        """ Sets the logger for the script """
        logger_path = os.path.join('data', 'bitcoin_value_logs.log')
        logger = logging.getLogger('bitcoin_value_logger')
        logger.setLevel(logging.INFO)
        if not logger.hasHandlers():
            file_handler = logging.FileHandler(logger_path)
            file_handler.setLevel(logging.INFO)
            formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formater)
            logger.addHandler(file_handler)
        return logger