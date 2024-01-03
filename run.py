# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

from dotenv import load_dotenv
import os
import requests

# Load variables from .env file
load_dotenv()

# Access API key from environment variable
api_key = os.getenv('API_KEY')

# User Interaction
def main():
    # User input stock ticker symbols via command line
    print("Welcome! This is a tiny financial analysis tool to help with your personal investment choices.")
    user_ticker = input("Enter a stock ticker symbol of interest. ")

    fetch_stock_data(user_ticker)


def fetch_stock_data(ticker):
    # Tool fetches stock data via api
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    print(data)


main()


# Data Analysis and Presentation
# - Perform basic calculations on the fetched data (e.g., average price, daily change)
# - Create a user menu to choose action
# - Display the analyzed data in a simple, textual format within the command line

# Exception Handling
# - Implement error handling to manage incorrect or empty inputs and API request failures
# - Ensure the tool communicates errors effectively to the user for a smoother experience