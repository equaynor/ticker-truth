import yfinance as yf
import pandas as pd
import time
import gspread
from google.oauth2.service_account import Credentials
import requests
from bs4 import BeautifulSoup
from termcolor import colored


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

# ANSI escape code for bold text
BOLD = "\033[1m"
# ANSI escape code to reset text formatting
RESET = "\033[0m"

USER_MENU = [1, 2, 3, 4, 5, 6]
BACK_TO_MENU = [1, 2]

welcome_message = """
    Are you ready to unlock the secrets of the stock market?
    Dive into the world of finance with Ticker Truth,
    your personal financial analysis tool!

    📊 Analyze the S&P 500 stock data, calculate daily changes,
    and track the 100-day moving average to make informed investment decisions.
    Whether you're a seasoned investor or just getting started,
    Ticker Truth is here to guide you on your financial journey.

    🔍 Enter your S&P 500 stock ticker symbols or company names of interest,
    explore historical data, and gain valuable insights.
    Check out your previous searches to see how your interests have evolved.

    🚀 Let's embark on this financial adventure together!
    Enter your name, choose a stock ticker,
    and let Ticker Truth empower your financial decisions.
    """


def typewriter_effect(text, delay=0.02):
    """
    Prints the provided text with a typewriter effect.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


# VALIDATION FUNCTIONS

def validate_ticker_symbol(input_value):
    """
    Validates the provided ticker symbol or company name.
    """
    df = create_stock_dataframe()
    input_value = input_value.upper().replace(" ", "")

    # Check if the input matches the ticker symbol or company name
    if input_value in df["Symbol"].values:
        return input_value
    elif input_value in df["Security"].str.replace(" ", "").str.upper().values:
        # Store df attributes in variable
        security = df["Security"].str.replace(" ", "").str.upper()
        # Get the corresponding ticker symbol for the company name
        ticker_symbols = df.loc[security == input_value, "Symbol"]
        if len(ticker_symbols) > 0:
            ticker_symbol = ticker_symbols.iloc[0]
            return ticker_symbol
    return None


def input_validation_loop():
    """
    Validates the user input for the ticker symbol
    or company name and loops if invalid.
    """

    while True:
        try:
            # Ask for user input
            user_input = input(BOLD +
                               "\nEnter a S&P 500 ticker symbol or company: " +
                               RESET)

            # Validate the user input for the ticker symbol or company name
            validated_ticker = validate_ticker_symbol(user_input)
            if validated_ticker:
                print(f"\n'{user_input}' " + colored("validated. ", "green") +
                      "Storing ticker symbol...")
                break
            else:
                print(colored(f"\nThe provided input ", "red") +
                      f"'{user_input}' " + colored("is invalid.", "red"))
                print("Please enter a valid S&P 500 ticker symbol or company.")
        except ValueError:
            print(colored(f"\nThe provided input ", "red") +
                  f"'{user_input}' " + colored("is invalid.", "red"))
            print("Please enter a valid S&P 500 ticker symbol or company.")
    return validated_ticker


def menu_option_validation(option_value, list_to_check):
    """
    Validates the user menu option input.
    """

    # Check if option value can be turned into int.
    try:
        option = int(option_value)
    except ValueError:
        print("\n" + colored("Invalid data: ", "red") +
              "Wrong numbers format, please try again.\n")
        return False

    # Checks if option value can't be found in list provided
    try:
        if option_value not in list_to_check:
            raise ValueError(
                "Value not recognised."
            )
    except ValueError:
        print("\n" + colored("Invalid data: ", "red") +
              "Please choose a number between 1 and " +
              f"{(len(list_to_check))}.\n")
        time.sleep(1)
        return False
    return True


# StORING AND RETRIEVING USER DATA FUNCTIONS

def store_user_name(name):
    """
    Store the user's name in a dictionary.
    """
    user_data = {"name": name, "ticker_searches": []}

    return user_data


def store_ticker_search_in_sheets(ud, ticker):
    """
    Stores username and ticker symbol in Google Sheets.
    """

    # Fetch all data from the sheet
    all_d = SHEET.worksheet(SHEET_NAME).get_all_values()

    # Search for ticker symbol in the local list or the Google Sheets
    if not any(ticker == row[1] for row in all_d[1:] if row[0] == ud['name']):

        # Append the data to the Google Sheets
        SHEET.worksheet(SHEET_NAME).append_row([ud['name'], ticker])

        print(colored("Successfully stored ", "green") +
              f"{ticker} " + colored("for ", "green") +
              f"{ud['name']}" + colored(".", "green"))

        # Store the ticker symbol in the local list
        ud['ticker_searches'].append(ticker)
    else:
        print(f"{ticker} is already stored for {ud['name']}.")


def show_previous_searches(ud):
    """
    Displays the previous searches for the user.
    """

    # Fetch all data from the sheet
    all_d = SHEET.worksheet(SHEET_NAME).get_all_values()

    print("\nRetrieving precious searches...\n")
    print(f"Previous searches for '{ud['name']}':")

    if len(all_d) > 1:  # Check if there are more rows than just the header
        prev_searches = (row[1] for row in all_d[1:] if row[0] == ud['name'])
        for ticker_symbol in prev_searches:
            print(ticker_symbol)

    else:
        print(colored("No previous searches found. \n", "red"))


# MENU FUNCTIONS

def user_menu(user_data, val_ticker):
    """
    Displays the user menu and handles user input.
    """

    choice = 0
    while choice != 6:
        print(BOLD + "\nPlease choose an option..." + RESET)
        time.sleep(0.5)
        print("1. Show latest stock data")
        print("2. Show daily change")
        print("3. Show 100 day moving average prices")
        print("4. Enter a new stock ticker symbol")
        print("5. Show previous searches")
        print("6. Quit \n")

        choice = int(input(BOLD +
                           "Please choose a number between 1 and 6: " +
                           RESET))
        if menu_option_validation(choice, USER_MENU):

            if choice == 1:
                print(f"\nRetrieving latest stock data for {val_ticker}...\n")
                time.sleep(1)
                fetch_latest_stock_data(val_ticker)
                back_to_menu(user_data, val_ticker)
                break

            elif choice == 2:
                print(f"\nCalculating daily change for {val_ticker}...\n")
                time.sleep(1)
                calculate_daily_change(val_ticker)
                back_to_menu(user_data, val_ticker)
                break

            elif choice == 3:
                print(f"\nCalculating 100 day m.a. for {val_ticker}...\n")
                time.sleep(1)
                calculate_100_day_average(val_ticker)
                back_to_menu(user_data, val_ticker)
                break

            elif choice == 4:
                new_ticker_symbol = input_validation_loop()
                print()
                store_ticker_search_in_sheets(user_data, new_ticker_symbol)
                user_menu(user_data, new_ticker_symbol)
                break

            elif choice == 5:
                show_previous_searches(user_data)
                back_to_menu(user_data, val_ticker)
                break

            elif choice == 6:
                print("\nQuitting Program...")
                time.sleep(1)
                print("Program terminated!")
                break
        break


def back_to_menu(user_data, val_ticker):
    """
    Displays the back to menu option and handles user input.
    """

    choice = 0
    while choice != 2:
        print("\n1. Back to menu")
        print("2. Quit\n")

        choice = int(input(BOLD +
                           "Please choose a number between 1 and 2: " +
                           RESET))
        if menu_option_validation(choice, BACK_TO_MENU):
            if choice == 1:
                time.sleep(1)
                user_menu(user_data, val_ticker)

            elif choice == 2:
                print("\nQuitting Program...")
                time.sleep(1)
                print("Program terminated!")
                break
        break


# ANALYSIS FUNCTIONS

def fetch_stock_data(validated_ticker, duration):
    """
    Fetches and returns the stock data for chosen stock ticker symbol.
    """

    # Fetch data for the provided ticker symbol
    stock_data = yf.Ticker(validated_ticker)

    # Fetch historical data
    historical_data = stock_data.history(period=duration)

    return historical_data


def fetch_latest_stock_data(validated_ticker):
    """
    Fetches and displays the latest stock data for chosen stock ticker symbol.
    """

    # Set stock data duration to one year
    historical_data = fetch_stock_data(validated_ticker, "1y")
    print(historical_data.head(1)[["Open", "High", "Low", "Close", "Volume"]])


def calculate_daily_change(validated_ticker):
    """
    Calculates and displays the daily change for chosen stock ticker symbol.
    """

    # Set stock data duration to one month
    his_data = fetch_stock_data(validated_ticker, "1mo")
    his_data["Daily Change"] = his_data["Close"] - his_data["Open"]

    print(his_data[["Open", "Close", "Daily Change"]])


def calculate_100_day_average(validated_ticker):
    """
    Calculates and displays the 100 day ma for chosen stock ticker symbol.
    """

    # Set stock data duration to one year
    his_data = fetch_stock_data(validated_ticker, "1y")
    his_data["100 Day MA"] = his_data["Close"].rolling(window=100).mean()

    print(his_data.tail(20)[["Close", "100 Day MA"]])


# STOCK TICKER WEB SCRAPER


URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
PAGE = requests.get(URL)

# Check if the request was successful (status code 200)
if PAGE.status_code == 200:
    html_text = PAGE.text
else:
    print(f"Failed to retrieve the webpage. Status code: {PAGE.status_code}")
    exit()


def create_stock_dataframe():
    """
    Creates a CSV file containing stock ticker data from the Wikipedia page.
    """

    # Parse the HTML text
    soup = BeautifulSoup(html_text, 'html.parser')

    # Extract the table
    table = soup.find_all('table', class_='wikitable sortable')[0]

    # Extract the table headers
    stock_titles = table.find_all('th')
    stock_titles = [title.text.strip() for title in stock_titles]

    # Create a dataframe to store the data
    df = pd.DataFrame(columns=stock_titles)

    # Extract the table data
    column_data = table.find_all('tr')

    for row in column_data[1:]:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]

        length = len(df)
        df.loc[length] = individual_row_data

    return df


# MAIN FUNCTION

def main():
    """
    Initiates the financial analysis tool,
    prompting the user for a username and a stock ticker symbol.
    The user's chosen stock ticker symbol will be stored
    in the global variable 'validated_ticker'.
    """
    print()
    print(BOLD + """
         *************************************************
        **  Welcome to Ticker Truth - Your Finance Ally"  **
         *************************************************
          """ + RESET)
    typewriter_effect(welcome_message)
    print(BOLD + """
         *************************************************
        **                Happy Investing!               **
         *************************************************
        """ + RESET)

    # Step 1: User Input Name
    user_name = input(BOLD + "Enter your name: ")
    print(f"\nWelcome, {user_name}!" + RESET)

    # Step 2: Name Storage
    user_data = store_user_name(user_name)

    # Step 3: User Input Ticker Symbol
    validated_ticker = input_validation_loop()

    # Step 4: Send to Google Sheet
    store_ticker_search_in_sheets(user_data, validated_ticker)

    # Step 5: Pass arguments to user menu
    user_menu(user_data, validated_ticker)


main()
