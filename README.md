### Task Details:
1. Objective: Write a Python script to fetch the current Bitcoin Price
Index (BPI) from a public API.
2. API: Use the CoinDesk API at
https://api.coinbase.com/v2/prices/BTC-USD/spot to retrieve the
current BPI.

### Requirements:
• The script should perform an HTTP GET request to the API endpoint.
• Extract the current Bitcoin price from the API response.
• Collect and save the Bitcoin price in USD every minute to a JSON
file.
• After collecting data for an hour, generate a graph of the Bitcoin Price
Index (BPI).
• Send an email using your Gmail account or any SMTP server with the
maximum Bitcoin price for the last hour.
