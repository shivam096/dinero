"""
stock_data_manager module: manange stock data (data from yfinance API).

Funtions:
    1. download_stock_data(ticker_symbol, period_str='5y')
    2. get_existing_tickers()
    3. update_stock_data()
    4. get_stock_data(ticker_symbol)
    5. get_filtered_stock_data(ticker_symbol, start_date='', end_date='')
    6. get_last_n_days(stock_data, n_days)
"""
import os

import pandas as pd
import yfinance as yf

DEFAULT_DATABASE_PATH = 'data'

def download_stock_data(ticker_symbol, period_str='5y'):
    """
    Function to download historical stock price data from Yahoo Finance.

    Parameters:
    ticker_symbol (str): The stock ticker symbol.
    period_str (str): The time period for which to fetch the data.
                      Accepted formats: 'max', '%dd', '%dwk', '%dmo', '%dy', case insensitive.
                      Defaults to '5y' (5 years).

    Returns:
    int: number of data points retrieved by yfinance.
        (length of DataFrame containing the historical stock price data)
        0 means unsuccess in retreiving data
        1 means possible invalid period_str input

    Side Effects:
    Save non-empty data to 'data/{ticker_symbol}.csv', do nothing otherwise.
    Print progress messages (complate or fail) to terminal.

    Exceptions:
    TypeError if ticker_symbol or period_str is not string
    ValueError if period_str has invalid format or ticker data not found.

    Example:
    >> download_stock_data("AAPL", "max")
    =================================================================================
    Notes:
    yfinance API does not raise Exceptions for invalid input or failed download,
    instead it prints error messgaes in terminal and returns empty pd.dataframe
    if ticker symbol not found or simply returns results with stock info of the
    latest available day if period string not recognized. Therefore, this wrap-up
    function returns the length of the retrieved data.

    sample Error messages:
    1 Failed download:
        ['MFT']: Exception('%ticker%: No data found, symbol may be delisted')
    """
    if not (isinstance(ticker_symbol, str) and isinstance(period_str, str)):
        raise TypeError("Arguments must be strings.")
    if not os.path.exists(DEFAULT_DATABASE_PATH):
        os.makedirs(DEFAULT_DATABASE_PATH)
    period_str = period_str.lower()
    ticker_symbol = ticker_symbol.upper()
    if not (period_str == 'max' or period_str[-1] in ['d','y']
            or period_str[-2:] in ['wk','mo']):
        raise ValueError("period format: 'max', 'd', 'wk', 'mo', 'y' (case insensitive).")

    data = yf.download(ticker_symbol, period=period_str)

    if len(data) == 0:
        raise ValueError("Fail to download: no data, ticker symbol may be delisted ")

    file_path = os.path.join(DEFAULT_DATABASE_PATH, f'{ticker_symbol}.csv')
    data.to_csv(file_path)
    return len(data)

def get_existing_tickers():
    """
    Function to retrieve a list of ticker symbol strings that exist in the data folder.

    Returns:
    list: A list of existing ticker symbol strings.
        Return empty list if data folder is empty.
    """
    return [file[:-4] for file in os.listdir(DEFAULT_DATABASE_PATH)
            if file.endswith('.csv')]

def update_stock_data():
    """
    Function to update the database. For each existing ticker, appending
    new data from the last recorded day to today to the original CSV file.

    Returns:
    list: list of updated ticker symbol strings.
    """
    existing_tickers = get_existing_tickers()
    for ticker_symbol in existing_tickers:
        file_path = os.path.join(DEFAULT_DATABASE_PATH, f'{ticker_symbol}.csv')
        existing_data = pd.read_csv(file_path)

        last_recorded_date = pd.to_datetime(existing_data['Date'].iloc[-1])
        last_recorded_date += pd.DateOffset(1)
        last_recorded_date = last_recorded_date.strftime('%Y-%m-%d')
        today = pd.Timestamp.today().strftime('%Y-%m-%d')

        new_data = yf.download(ticker_symbol, start=last_recorded_date, end=today)
        new_data.to_csv(file_path, mode='a', header=False)

    return existing_tickers

def get_stock_data(ticker_symbol):
    """
    Function to fetch stock data for a given ticker symbol from statistic database.

    Parameters:
    ticker_symbol (str): The stock ticker symbol.

    Returns:
    pd.DataFrame: A DataFrame containing the stock data.

    Exceptions:
    TypeError if ticker_symbol is not a string
    ValueError if ticker not in database
    """
    if not isinstance(ticker_symbol, str):
        raise TypeError("ticker symbol must be strings.")
    ticker_symbol = ticker_symbol.upper()
    file_path = os.path.join(DEFAULT_DATABASE_PATH, f'{ticker_symbol}.csv')
    if not os.path.exists(file_path):
        raise ValueError("No such database. Please download initial data first.")
    return pd.read_csv(file_path)

def get_filtered_stock_data(ticker_symbol, start_date='1900-01-01', end_date=''):
    """
    Function to fetch stock data of the ticker within given timeframe from statistic database.

    Parameters:
    ticker_symbol (str): The stock ticker symbol.
    start_date (str, optional): The start date for the filtered data in 'yyyy-mm-dd' format.
                                (inclusive) Defaults to '1900-01-01'.
    end_date (str, optional): The end date for the filtered data in 'yyyy-mm-dd' format.
                              (inclusive) Defaults to ''.

    Returns:
    pd.DataFrame: A DataFrame containing the filtered stock data.

    Exceptions:
    TypeError:
        If start_date or end_data is not string
    ValueError:
        If start_date or end_date has invalid date format
        or start_date is later than end_date.
    """
    stock_data = get_stock_data(ticker_symbol)

    if not (isinstance(start_date, str) and isinstance(end_date, str)):
        raise TypeError("Dates must be strings in form of 'yyyy-mm-dd'.")

    if len(start_date.strip()) == 0:
        start_date = '1900-01-01'
    start_date = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce')
    if pd.isnull(start_date):
        raise ValueError("Valid Format of start date should be 'yyyy-mm-dd'.")
    if len(end_date.strip()) == 0:
        end_date = pd.Timestamp.today() + pd.DateOffset(1)
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce')
    if pd.isnull(end_date):
        raise ValueError("Valid Format of end date should be 'yyyy-mm-dd'.")

    if start_date > end_date:
        raise ValueError("Start date after end date.")

    return stock_data.query(f"'{start_date}' <= Date <= '{end_date}'")

def get_last_n_days(stock_data, n_days):
    """
    Extracts the last n_days rows from the DataFrame.

    Parameters:
        stock_data (DataFrame): Input DataFrame.
        n_days (int): Number of days from the end of the DataFrame.

    Returns:
        DataFrame: DataFrame containing the last n_days rows, or the entire
        DataFrame if n_days exceeds the number of rows.

    Exceptions:
    ValueError if the number of days entered is a negative integer or 0.
    TypeError if stock_data is not pd.DataFrame or n_days is not an integer
    """
    # Ensure stock_data is a dataframe and n_days is a positive integer
    if not isinstance(stock_data, pd.DataFrame):
        raise TypeError("data must be pandas dataframe")
    if not isinstance(n_days, int):
        raise TypeError("Number of Days must be an Integer")
    if n_days <= 0:
        raise ValueError("Number of days must be a positive integer")

    # Check if n_days exceeds the number of rows in the DataFrame
    if n_days >= len(stock_data):
        return stock_data  # Return the entire DataFrame

    # Get the last n_days rows from the DataFrame
    last_n_days_df = stock_data.iloc[-n_days:]

    return last_n_days_df
