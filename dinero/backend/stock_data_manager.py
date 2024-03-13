"""
stock_data_manager module: manange stock data (data from yfinance API).

Funtions:
    1. download_stock_data(ticker_symbol, period_str='5y')
    2. get_existing_tickers()
    3. update_stock_data()
    4. get_stock_data(ticker_symbol)
    5. get_filtered_stock_data(ticker_symbol, start_date='', end_date='')
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
    period_str = period_str.lower()
    ticker_symbol = ticker_symbol.upper()
    data = yf.download(ticker_symbol, period=period_str)

    if len(data) == 0:
        return len(data)

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
    return [file[:-4] for file in os.listdir('data') if file.endswith('.csv')]

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
    """
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

    Raises:
    ValueError:
        If start_date is later than end_date.
    """
    stock_data = get_stock_data(ticker_symbol)

    start_date = pd.to_datetime(start_date, format='%Y-%m-%d')

    if len(end_date) == 0:
        end_date = pd.Timestamp.today() + pd.DateOffset(1)
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

    if start_date > end_date:
        raise ValueError("Start date after end date.")

    return stock_data.query(f"'{start_date}' <= Date <= '{end_date}'")

def get_last_n_days(df, n_days):
    """
    Extracts the last n_days rows from the DataFrame.

    Parameters:
        df (DataFrame): Input DataFrame.
        n_days (int): Number of days from the end of the DataFrame.

    Returns:
        DataFrame: DataFrame containing the last n_days rows, or the entire
        DataFrame if n_days exceeds the number of rows.


    Raises:
    ValueError:
        If the number of days entered is a negative integer or 0.
    TypeError:
        If the number of days enetered is not an integer
    """

    # Ensure n_days is a positive integer
    if not isinstance(n_days, int):
        raise TypeError("Number of Days must be an Integer")
    if n_days <= 0:
        raise ValueError("Number of days must be a positive integer")

    # Check if n_days exceeds the number of rows in the DataFrame
    if n_days >= len(df):
        return df  # Return the entire DataFrame

    # Get the last n_days rows from the DataFrame
    last_n_days_df = df.iloc[-n_days:]

    return last_n_days_df
