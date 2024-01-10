# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import yfinance as yf


# User Interaction
def main():
    # User input stock ticker symbols via command line
    print("Welcome! This is a tiny financial analysis tool to help with your personal investment choices.")
    global user_ticker
    user_ticker = input("Enter a stock ticker symbol of interest. ")

    fetch_stock_data(user_ticker)
    user_menu(user_ticker)


def user_menu(user_ticker):
    # Create a choice list for the user to choose from

    choice = 0
    while choice != 5:
        print("Please choose an option...")
        print("1. Show latest stock data")
        print("2. Show daily change")
        print("3. Show 100 day average price")
        print("4. Enter a new stock ticker symbol")
        print("5. Quit")
        choice = int(input())

        if choice == 1:
            print(f"Retrieving latest stock data for {user_ticker}...")
            fetch_latest_stock_data(user_ticker)
            back_to_menu()
            break
            
        elif choice == 2:
            print(f"Calculating daily change for {user_ticker}...")
            calculate_daily_change(user_ticker)
            back_to_menu()
            break

        elif choice == 3:
            print(f"Calculating 100 day average for {user_ticker}...")
            calculate_100_day_average(user_ticker)
            back_to_menu()
            break

        elif choice == 4:
            main()

        elif choice == 5:
            print("Quitting Program...")
    print("Program terminated!")


def fetch_stock_data(ticker, duration):
    # Fetch data for the provided ticker symbol
    stock_data = yf.Ticker(ticker)

    # Fetch historical data
    historical_data = stock_data.history(period=duration)

    return historical_data


def fetch_latest_stock_data(ticker):

    print(historical_data.head(1)[["Open", "High", "Low", "Close", "Volume"]])

    
def back_to_menu():
    
    choice = 0
    while choice != 2:
        print("1. Back to menu")
        print("2. Quit")
        choice = int(input())
        
        if choice == 1:
            user_menu(user_ticker)
        
        elif choice == 2:
            print("Quitting Program...")
    

def calculate_daily_change(ticker):
    
    stock_data = yf.Ticker(ticker)
    
    historical_data = stock_data.history(period="1mo")
    historical_data["Daily Change"] = historical_data["Close"] - historical_data["Open"]
    
    print(historical_data[["Open", "Close", "Daily Change"]])
    

def calculate_100_day_average(ticker):
    
    historical_data["100 Day MA"] = historical_data["Close"].rolling(window=100).mean()

    print(historical_data.tail(20)[["Close", "100 Day MA"]])

main()


# Data Analysis and Presentation
# - Perform basic calculations on the fetched data (e.g., average price, daily change)
# - Create a user menu to choose action
# - Display the analyzed data in a simple, textual format within the command line

# Exception Handling
# - Implement error handling to manage incorrect or empty inputs and API request failures
# - Ensure the tool communicates errors effectively to the user for a smoother experience