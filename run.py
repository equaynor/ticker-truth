# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import yfinance as yf


# User Interaction
def main():
    """
    Initiates the financial analysis tool, prompting the user for a stock ticker symbol.
    The user's chosen stock ticker symbol will be stored in the global variable 'user_ticker'.
    """
    
    print("Welcome! This is a tiny financial analysis tool to help with your personal investment choices.")
    global user_ticker
    user_ticker = input("Enter a stock ticker symbol of interest. ")

    user_menu()


def user_menu():
    """
        Displays a menu for the user to choose from various financial analysis options.

        The user can choose to view the latest stock data, calculate daily changes, 
        calculate the 100-day average, enter a new stock ticker symbol, or quit the program.
        """

    choice = 0
    while choice != 5:
        print("Please choose an option...")
        print("1. Show latest stock data")
        print("2. Show daily change")
        print("3. Show 100 day average price")
        print("4. Enter a new stock ticker symbol")
        print("5. Quit")
        
        try:
            choice = int(input())
            
            if choice < 1 or choice > 5:
                raise ValueError
        
        except ValueError:
            print("Please choose a number between 1 and 5.")
        
        else:
            if choice == 1:
                print(f"Retrieving latest stock data for {user_ticker}...")
                fetch_latest_stock_data()
                back_to_menu()
                break
                
            elif choice == 2:
                print(f"Calculating daily change for {user_ticker}...")
                calculate_daily_change()
                back_to_menu()
                break

            elif choice == 3:
                print(f"Calculating 100 day average for {user_ticker}...")
                calculate_100_day_average()
                back_to_menu()
                break

            elif choice == 4:
                main()

            elif choice == 5:
                print("Quitting Program...")
    print("Program terminated!")


def back_to_menu():
    """
    Provides options to the user to either go back to the main menu or quit the program.
    """
    
    choice = 0
    while choice != 2:
        print("1. Back to menu")
        print("2. Quit")
        
        try:
            choice = int(input())
            
            if choice < 1 or choice > 2:
                raise ValueError
        
        except ValueError:
            print("Please choose a number 1 or number 2.")
        
        else:
            if choice == 1:
                user_menu()
            
            elif choice == 2:
                print("Quitting Program...")
            

def fetch_stock_data(duration):
    """
    Fetches historical stock data for the specified duration.

    Parameters:
    - duration (str): The duration for which historical data should be fetched (e.g., "1y", "1mo").

    Returns:
    pd.DataFrame: Historical stock data.
    """
    
    # Fetch data for the provided ticker symbol
    stock_data = yf.Ticker(user_ticker)

    # Fetch historical data
    historical_data = stock_data.history(period=duration)

    return historical_data


def fetch_latest_stock_data():
    """
    Fetches and displays the latest stock data for the user's chosen stock ticker symbol.

    Displays the Open, High, Low, Close, and Volume of the latest available stock data.
    """
    
    # Set stock data duration to one year
    historical_data = fetch_stock_data("1y")
    print(historical_data.head(1)[["Open", "High", "Low", "Close", "Volume"]])
    

def calculate_daily_change():
    """
    Calculates and displays the daily change for the user's chosen stock ticker symbol.

    Calculates the difference between the Close and Open prices for each day in the last month.
    """
    
    # Set stock data duration to one month
    historical_data = fetch_stock_data("1mo")
    historical_data["Daily Change"] = historical_data["Close"] - historical_data["Open"]
    
    print(historical_data[["Open", "Close", "Daily Change"]])
    

def calculate_100_day_average():
    """
    Calculates and displays the 100-day moving average for the user's chosen stock ticker symbol.

    Calculates the 100-day moving average based on the closing prices of the last year's data.
    """
    
    # Set stock data duration to one year
    historical_data = fetch_stock_data("1y")
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