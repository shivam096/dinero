import pandas as pd

# Simple Moving Average
def calculate_simple_moving_average(df, length):
    return df['Close'].rolling(window=length).mean()

#Relative Strength Index
def calculate_rsi(df, length=14):
    delta = df['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

#Rate of Change
def calculate_roc(df, length=14):
    roc = ((df['Close'] - df['Close'].shift(length)) / df['Close'].shift(length)) * 100
    return roc

#Bollinger Bands %
def calculate_bollinger_bands_percent(df, length=20, num_std_dev=2):
    sma = df['Close'].rolling(window=length).mean()
    std_dev = df['Close'].rolling(window=length).std()

    upper_band = sma + (std_dev * num_std_dev)
    lower_band = sma - (std_dev * num_std_dev)

    percent_b = (df['Close'] - lower_band) / (upper_band - lower_band)
    return percent_b


