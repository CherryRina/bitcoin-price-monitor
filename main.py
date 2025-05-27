import logging
import requests
import sched
import time
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  matplotlib import pyplot as plt
from datetime import datetime as dt
from matplotlib.ticker import FuncFormatter
from dotenv import load_dotenv


# --- Load Private & Environment Variables ---
load_dotenv() 
BITCOIN_ENDPOINT = os.getenv("BITCOIN_ENDPOINT")
FILE_NAME = 'bitcoin_prices.json'

# --- LOGGER Setup ---

LOGGER = setup_LOGGER()  # global access to the LOGGER




# --- Bitcoin Price ---
def get_bitcoin_price():
    """ Starts an api get request and creates new json entry out of the responce """
    try:
        # get request to bitcoin url
        # collect data
        bitcoin_price = float(bitcoin_response.json()["data"]["amount"])
        timestamp = dt.now().strftime('%H:%M:%S')
        # save data in json file
        save_price(timestamp, bitcoin_price)
        # schedule
    except Exception as e:
        log_by_level(30, "Failed to fetch Bitcoin price: {e}. Will retry again in 60 seconds")


def save_price(timestamp, bitcoin_price):
    """ Recieves a new entry and inserts it into the Bitcoin price json file """
    # load existing json file
    json_data = safe_load_json(FILE_NAME)
    # create and convert updated data into json file
    json_data[timestamp] = bitcoin_price
    with open(FILE_NAME, "w")  as file:
        json.dump(json_data, file, indent=4)

    # schduler
    log_by_level(20, "Price was added")

    



# --- EMail Sender ---
def find_max_price():
    """ Finds max Bitcoin price inside json, returns the prices value and time """
    json_data = safe_load_json(FILE_NAME)
    if not json_data:
        return "Could not determine max Bitcoin price."
    max_row = max(json_data, key=lambda x: json_data[x])
    price = f"{json_data[max_row]:,}"
    result = f"Maximum Bitcoin price in the past hour was ${price} at {max_row}."
    return result



# --- Main ---
def main():
    """ main function """

    log_by_level(20, "Started running...")



if __name__ == "__main__":
    main()