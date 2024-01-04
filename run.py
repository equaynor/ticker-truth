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
    print(data)
    user_menu()


def user_menu():
    # Create a choice list for the user to choose from

    choice = 0
    while choice != 5:
        print("Please choose an option...")
        print("1. Show live price")
        print("2. Show daily change")
        print("3. Show 100 day average price")
        print("4. Enter a new stock ticker symbol")
        print("5. Quit")
        choice = int(input())

        if choice == 1:
            print(f"Retrieving live price for {user_ticker}")
            # show_live_price(user_ticker)

        elif choice == 2:
            print(f"Calculating daily change for {user_ticker}")
            # calculate_daily_change(user_ticker)

        elif choice == 3:
            print(f"Calculating 100 day average for {user_ticker}")
            # calculate_100_day_average(user_ticker)

        elif choice == 4:
            main()

        elif choice == 5:
            print("Quitting Program")
    print("Program terminated!")


def fetch_stock_data(ticker):
    # Tool fetches stock data via api
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}'
    r = requests.get(url)
    global data
    data = r.json()


# def show_live_price(ticker):


# def calculate_daily_change(ticker):


# def calculate_100_day_average(ticker):


main()


# Data Analysis and Presentation
# - Perform basic calculations on the fetched data (e.g., average price, daily change)
# - Create a user menu to choose action
# - Display the analyzed data in a simple, textual format within the command line

# Exception Handling
# - Implement error handling to manage incorrect or empty inputs and API request failures
# - Ensure the tool communicates errors effectively to the user for a smoother experience