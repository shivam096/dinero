"""
Funtions:
    1. download_stock_data(ticker_symbol, period_str)
    2. update_stock_data(ticker_symbol)
"""
import os

import pandas as pd
import yfinance as yf

"""
download_stock_data("AAPL", "5y")

ticker_symbol
period_str: '1y' = one year, '1m' = one month, '1d' = one day
"""
def download_stock_data(ticker_symbol, period_str):
    # Create data folder if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Download data from Yahoo Finance
    data = yf.download(ticker_symbol, period=period_str)

    # Save data to CSV file
    file_path = f'data/{ticker_symbol}.csv'
    data.to_csv(file_path)

"""
update_stock_data('AAPL')

ticker_symbol: exsiting ticker
(one of 'AAPL', 'GOOG', 'MSFT', 'NVDA', 'TSLA' in  this case)
"""
def update_stock_data(ticker_symbol):  
    file_path = f'data/{ticker_symbol}.csv'

    # Check if CSV file exists
    if not os.path.exists(file_path):
        raise ValueError('No such ticker. Please download initial data first.')
    else:
        existing_data = pd.read_csv(file_path)

        last_updated_date = existing_data['Date'].iloc[-1]
        last_updated_date = pd.to_datetime(last_updated_date)
        last_updated_date += pd.DateOffset(1)
        last_updated_date = last_updated_date.strftime('%Y-%m-%d')
        today = pd.Timestamp.today().strftime('%Y-%m-%d')

        # Download new data from Yahoo Finance
        new_data = yf.download(ticker_symbol, start=last_updated_date, end=today)

        # Update the database
        new_data.to_csv(file_path, mode='a', header=False)


# Fetch stock data
def get_stock_data(symbol):  # start_date, end_date
    file_path = f"dinero/data/{symbol}.csv"
    # Check if CSV file exists
    if not os.path.exists(file_path):
        raise ValueError('No such ticker. Please download initial data first.')
    stock_data = pd.read_csv(file_path)
    return stock_data
