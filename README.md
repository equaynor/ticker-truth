# Ticker Truth - Financial Analysis Tool

  - [Overview](#overview)
  - [UX/UI](#uxui)
    - [Strategy](#strategy)
      - [Goals](#goals)
      - [User Stories](#user-stories)
    - [Scope](#scope)
    - [Structure](#structure)
    - [Flowcharts](#flowcharts)
    - [Surface/Design](#surfacedesign)
      - [Welcome Message](#welcome-message)
      - [User Input and Validation](#user-input-and-validation)
      - [Order Overview](#order-overview)
      - [Live Status](#live-status)
  - [Features](#features)
    - [Existing Features](#existing-features)
    - [Future Features](#future-features)
  - [Bugs or Errors](#bugs-or-errors)
  - [Testing](#testing)
  - [Modules Imported](#modules-imported)
  - [Deployment](#deployment)
    - [Creating the Tool](#creating-the-tool)
    - [Deploying on Heroku](#deploying-on-heroku)
    - [Fork the Repository](#fork-the-repository)
    - [Clone the Repository](#clone-the-repository)
  - [Credits](#credits)
  - [Tools](#tools)
  - [Acknowledgements](#acknowledgements)

## Overview

Tapping into the vast realm of financial data, Ticker Truth empowers users to analyze stock ticker symbols and gain valuable insights. The tool's robust features include the ability to input and validate stock ticker symbols, view detailed financial data tables, and receive real-time analysis results.

## UX/UI

### Strategy

#### Goals

- **Intuitive User Experience:** Ensure a user-friendly interface for easy navigation.
- **Relevant Information:** Display pertinent information at each step of the analysis.
- **Clear Instructions:** Provide concise and clear instructions for seamless interaction.
- **Highlight Important Information:** Emphasize crucial details for an enhanced user experience.
- **Input Validation:** Ensure the user inputs existing stock tickers or companies.
- **Data Accuracy:** Access the correct data for accurate analysis and updates.
- **Duration Calculation:** Calculate and display a sensible duration for each analysis.
- **Search History:** Store and display the user's search history.

#### User Stories

- As a user, I want to be able to enter and save my username.
- As a user, I want to be able to enter a stock ticker symbol or company name.
- As a user, I want to be able to get the latest stock data for that ticker symbol
- As a user, I want to be able to calculate the daily change for a stock ticker symbol.
- As a user, I want to be able to calculate the 100 day moving average for a stock ticker symbol.
- As a user, I want to be able to see a list of my previous searches.
- As a user, I want to be able to enter a new stock ticker symbol and have it added to my list of previous searches.
- As a user, I want to be able to go back to the user menu.
- As a user, I want to be able to quit the program at any time.

### Scope

Ticker Truth covers a broad spectrum of features to meet users' analytical needs:

- **Financial Data Display:** Present detailed financial data tables for thorough analysis.
- **User Input and Validation:** Allow users to input stock ticker symbols or company names and validate them.
- **Warning System:** Implement a warning system for invalid inputs to enhance user accuracy.
- **Analysis Results:** Calculate and display insightful results based on the inputted stock.
- **Google Sheets Integration:** Store each user's search history in a Google Sheet.
- **History Overview:** Provide a list of the user'sprevious searches for quick reference.

### Structure

Ticker Truth uses a mock terminal, leveraging the Code Institute Python Template. The entire code was written in Python and resides in the `run.py` file, which is what Heroku will run when the program is used.

