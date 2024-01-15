import yfinance as yf
import pyfiglet
import time
import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ticker-history')
SHEET_NAME = 'Ticker Searches'


# User Interaction
def main():
    """
    Initiates the financial analysis tool, prompting the user for a stock ticker symbol.
    The user's chosen stock ticker symbol will be stored in the global variable 'user_ticker'.
    """
    
    print_ascii_art()
    print("""
          *************************************************
         **  Welcome to Ticker Truth - Your Finance Ally  **
          *************************************************
          """)
    typewriter_effect(welcome_message)
    
    # Step 1: User Input Name
    user_name = input("Enter your name: ")

    # Step 2: Name Storage
    user_data = store_user_name(user_name)
    
    # Step 3: User Input Ticker Symbol
    user_ticker = input("\n Enter a stock ticker symbol of interest. \n")

    # Step 4: Send to Google Sheet
    store_ticker_search_in_sheets(user_data, user_ticker)

    # Step 5: Pass arguments to user menu
    user_menu(user_data, user_ticker)


def print_ascii_art():
    
    text = pyfiglet.figlet_format(text="Ticker Truth",
                                  font="rozzo")
    
    print("\n")
    print(text)


def typewriter_effect(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


welcome_message = """
    Are you ready to unlock the secrets of the stock market? Dive into the world of finance with Ticker Truth, your personal financial analysis tool!

    📊 Analyze stock data, calculate daily changes, and track the 100-day moving average to make informed investment decisions. Whether you're a seasoned investor or just getting started, Ticker Truth is here to guide you on your financial journey.

    🔍 Enter your stock ticker symbols, explore historical data, and gain valuable insights. Plus, check out your previous searches to see how your interests have evolved over time.

    🚀 Let's embark on this financial adventure together! Enter your name, choose a stock ticker, and let Ticker Truth empower your financial decisions.

      *************************************************
     **                Happy Investing!               **
      *************************************************
    """


def store_user_name(name):

    user_data = {"name": name, "ticker_searches": []}

    return user_data


def store_ticker_search_in_sheets(user_data, ticker_symbol):
    """
    Store the user's ticker search in Google Sheets.
    """

    # Fetch all data from the sheet
    all_data = SHEET.worksheet(SHEET_NAME).get_all_values()

    # Check if the ticker symbol is already present in the local list or the Google Sheets
    if not any(ticker_symbol == row[1] for row in all_data[1:] if row[0] == user_data['name']):

        # Append the data to the Google Sheets
        SHEET.worksheet(SHEET_NAME).append_row([user_data['name'], ticker_symbol])

        print(f"Successfully stored {ticker_symbol} for {user_data['name']}.")
    else:
        print(f"{ticker_symbol} is already stored for {user_data['name']}.")


def user_menu(user_data, user_ticker):
    """
        Displays a menu for the user to choose from various financial analysis options.

        The user can choose to view the latest stock data, calculate daily changes, 
        calculate the 100-day average, enter a new stock ticker symbol, show previous searches, or quit the program.
        """

    choice = 0
    while choice != 6:
        print("Please choose an option...")
        print("1. Show latest stock data")
        print("2. Show daily change")
        print("3. Show 100 day average price")
        print("4. Enter a new stock ticker symbol")
        print("5. Show previous searches")
        print("6. Quit")
        
        try:
            choice = int(input())
            
            if choice < 1 or choice > 5:
                raise ValueError
        
        except ValueError:
            print("Please choose a number between 1 and 5.")
        
        else:
            if choice == 1:
                print(f"Retrieving latest stock data for {user_ticker}...")
                fetch_latest_stock_data(user_ticker)
                back_to_menu(user_data, user_ticker)
                break
                
            elif choice == 2:
                print(f"Calculating daily change for {user_ticker}...")
                calculate_daily_change(user_ticker)
                back_to_menu(user_data, user_ticker)
                break

            elif choice == 3:
                print(f"Calculating 100 day average for {user_ticker}...")
                calculate_100_day_average(user_ticker)
                back_to_menu(user_data, user_ticker)
                break

            elif choice == 4:
                new_ticker_symbol = input("Enter a new stock ticker symbol: ")
                store_ticker_search_in_sheets(user_data, new_ticker_symbol)
                user_menu(user_data, new_ticker_symbol)

            elif choice == 5:
                show_previous_searches(user_data)
                back_to_menu(user_data, user_ticker)
                break

            elif choice == 6:
                print("Quitting Program...")
    print("Program terminated!")


def back_to_menu(user_data, user_ticker):
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
                user_menu(user_data, user_ticker)
            
            elif choice == 2:
                print("Quitting Program...")
            

def fetch_stock_data(user_ticker, duration):
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


def fetch_latest_stock_data(user_ticker):
    """
    Fetches and displays the latest stock data for the user's chosen stock ticker symbol.

    Displays the Open, High, Low, Close, and Volume of the latest available stock data.
    """
    
    # Set stock data duration to one year
    historical_data = fetch_stock_data(user_ticker, "1y")
    print(historical_data.head(1)[["Open", "High", "Low", "Close", "Volume"]])
    

def calculate_daily_change(user_ticker):
    """
    Calculates and displays the daily change for the user's chosen stock ticker symbol.

    Calculates the difference between the Close and Open prices for each day in the last month.
    """
    
    # Set stock data duration to one month
    historical_data = fetch_stock_data(user_ticker, "1mo")
    historical_data["Daily Change"] = historical_data["Close"] - historical_data["Open"]
    
    print(historical_data[["Open", "Close", "Daily Change"]])
    

def calculate_100_day_average(user_ticker):
    """
    Calculates and displays the 100-day moving average for the user's chosen stock ticker symbol.

    Calculates the 100-day moving average based on the closing prices of the last year's data.
    """
    
    # Set stock data duration to one year
    historical_data = fetch_stock_data(user_ticker, "1y")
    historical_data["100 Day MA"] = historical_data["Close"].rolling(window=100).mean()

    print(historical_data.tail(20)[["Close", "100 Day MA"]])


def show_previous_searches(user_data):

    # Fetch all data from the sheet
    all_data = SHEET.worksheet(SHEET_NAME).get_all_values()

    print(f"Previous searches for {user_data['name']}:")

    if len(all_data) > 1:  # Check if there are more rows than just the header
        previous_searches = (row[1] for row in all_data[1:] if row[0] == user_data['name'])
        for ticker_symbol in previous_searches:
            print(ticker_symbol)
        
    else:
        print("No previous searches found.")


main()
