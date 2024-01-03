# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import yahoo_fin.stock_info as si


# User Interaction
# - User input stock ticker symbols via command line

print("Welcome! This is a tiny financial analysis tool to help with your personal investment choices.")
ticker = input("Enter a stock ticker symbol of interest. ")

# - Tool fetches stock data via api

ticker_data = si.get_data(ticker)

# Data Analysis and Presentation
# - Perform basic calculations on the fetched data (e.g., average price, daily change)
# - Create a user menu to choose action
# - Display the analyzed data in a simple, textual format within the command line

# Exception Handling
# - Implement error handling to manage incorrect or empty inputs and API request failures
# - Ensure the tool communicates errors effectively to the user for a smoother experience