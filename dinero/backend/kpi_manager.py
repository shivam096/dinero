"""
This module provides functionalities to read stock data from CSV files and
compute various technical indicators such as Simple Moving Average (MA),
Relative Strength Index (RSI), Rate of Change (ROC), and Bollinger Bands Percent (BBP)
by utilizing the technical_indicators module.
"""
import os
import pandas as pd
import backend.technical_indicators as ti

from backend.stock_data_manager import get_stock_data

# Fetches Technical Indicator
def get_technical_indicator(ticker_symbol, length, indicator):
    """Fetches technical indicators from the technical_indicators module"""
    stock_data = get_stock_data(ticker_symbol)

    if indicator == 'MA':
        return ti.calculate_simple_moving_average(stock_data, length).dropna()
    if indicator == 'RSI':
        return ti.calculate_rsi(stock_data, length).dropna()
    if indicator == 'ROC':
        return ti.calculate_roc(stock_data, length).dropna()
    if indicator == 'BBP':
        return ti.calculate_bollinger_bands_percent(stock_data, length).dropna()

    raise ValueError("Unsupported indicator. Please use 'MA','RSI','ROC' or 'BBP'.")
