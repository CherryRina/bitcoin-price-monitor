import logging

class Logger():
    def __init__(self):
        self.logger = self.setup_logger()


    def setup_logger(self):
        """ Sets the logger for the script """
        # logger
        logger = logging.getLogger('bitcoin_value_logger')
        logger.setLevel(logging.INFO)
        if not logger.hasHandlers():
            # handler
            file_handler = logging.FileHandler('bitcoin_value_logs.log')
            file_handler.setLevel(logging.INFO)
            # formatter
            formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formater)
            # add handler to logger 
            logger.addHandler(file_handler)
            logger.info("New logger file was created")
        return logger