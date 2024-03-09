"""Module for calculating various technical indicators used in financial analysis."""
import pandas as pd


# Simple Moving Average
def calculate_simple_moving_average(data, length):
    """Calculates the Simple Moving Average (SMA) of the 'Close' prices over a specified length."""
    moving_avg = data['Close'].rolling(window=length).mean()
    return _formatted_dataframe(data, moving_avg, 'MA')


# Relative Strength Index
def calculate_rsi(data, length=14):
    """Computes the Relative Strength Index (RSI) for the 'Close' prices over a specified length."""
    delta = data['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    relative_s = gain / loss
    rsi = 100 - (100 / (1 + relative_s))

    return _formatted_dataframe(data, rsi, 'RSI')


# Rate of Change
def calculate_roc(data, length=14):
    """Determines the Rate of Change (ROC) of the 'Close' prices over a specified length."""
    roc = ((data['Close'] - data['Close'].shift(length)) / data['Close'].shift(length)) * 100
    return _formatted_dataframe(data, roc, 'ROC')


# Bollinger Bands %
def calculate_bollinger_bands_percent(data, length=20, num_std_dev=2):
    """Calculates the Bollinger Bands Percentage (BBP) for the 'Close' prices
    over a specified length."""
    sma = data['Close'].rolling(window=length).mean()
    std_dev = data['Close'].rolling(window=length).std()

    upper_band = sma + (std_dev * num_std_dev)
    lower_band = sma - (std_dev * num_std_dev)

    percent_b = (data['Close'] - lower_band) / (upper_band - lower_band)
    return _formatted_dataframe(data, percent_b, 'BBP')


def _formatted_dataframe(data, indicator, name):
    """Formats the resulting DataFrame by appending the date and the calculated indicator."""
    result_df = pd.DataFrame()
    result_df['Date'] = data['Date']
    result_df[name] = indicator
    return result_df
