"""
This module provides functionalities to read stock data from CSV files and
compute various technical indicators such as Simple Moving Average (MA),
Relative Strength Index (RSI), Rate of Change (ROC), and Bollinger Bands Percent (BBP)
by utilizing the technical_indicators module.
"""
import os
import pandas as pd
import dinero.backend.technical_indicators as ti


# Reads Stock data
def read_stock_data(stock_symbol):
    """Reads stock data from CSV file."""
    file_path = f"dinero/data/{stock_symbol}.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No data file found for stock symbol: {stock_symbol}")
    return pd.read_csv(file_path)


# Fetches Technical Indicator
def get_technical_indicator(ticker_symbol, length, indicator):
    """Fetches technical indicators from the technical_indicators module"""
    stock_data = read_stock_data(ticker_symbol)

    if indicator == 'MA':
        return ti.calculate_simple_moving_average(stock_data, length).dropna()
    if indicator == 'RSI':
        return ti.calculate_rsi(stock_data, length).dropna()
    if indicator == 'ROC':
        return ti.calculate_roc(stock_data, length).dropna()
    if indicator == 'BBP':
        return ti.calculate_bollinger_bands_percent(stock_data, length).dropna()

    raise ValueError("Unsupported indicator. Please use 'MA','RSI','ROC' or 'BBP'.")
