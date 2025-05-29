# Bitcoin Price Index Tracker
A Python application that monitors Bitcoin prices in real-time, collects hourly data, generates price graphs, and sends email notifications with price analytics.

## Overview
This application fetches the current Bitcoin Price Index (BPI) from the CoinDesk API every minute, stores the data locally, and after collecting an hour's worth of data, generates a price graph and emails a summary with the maximum price recorded.


## Classes Architecture
- **`BitcoinPriceManager`**: Handles API requests to Bitcoin endpoint and manages data saving to JSON
- **`EmailManager`**: Parses price according to mail, creates email messages, and sends notifications
- **`BitcoinGraphGenerator`**: Creates graph images and saves them
- **`JsonHandler`**: Provides safe JSON file operations with comprehensive error handling
- **`logger`**: Sets up application logging

## Installation

### Prerequisites
- Python 3.7 or higher
- Gmail account or SMTP server access

### Create environment file
   Sensitive information is stored in .env file.
   Create a `.env` file in the root directory with the following variables:
   ```env
   DST_EMAIL=recipient@example.com
   BITCOIN_ENDPOINT=https://api.coindesk.com/v1/bpi/currentprice.json
   SRC_EMAIL=your-email@gmail.com
   SRC_EMAIL_PASSWORD=your-app-password
   ```

## Usage

### Running the Application
Execute the main script from the project root:

### Application Workflow
1. **Data Collection**: The script fetches Bitcoin prices every minute
2. **Data Storage**: Prices are stored in JSON files in the `/data` directory
3. **Hourly Processing**: After one hour of data collection:
   - A price graph is generated and saved to `/graph_images`
   - The maximum price for the hour is calculated
   - An email notification is sent with the price summary

### Output Files
- **JSON Data**: `data/bitcoin_prices.json` - Contains timestamped price data
- **Log Files**: `data/bitcoin_value_logs.log` - Application logs for monitoring and debugging
- **Graph Images**: `graph_images/*.png` - Generated price charts
