import pandas as pd
import technical_indicators as ti

#Reads Stock data
def read_stock_data(stock_symbol):
    """Read stock data from CSV file."""
    file_path = f'../data/{stock_symbol}.csv'  # Adjust path as needed
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    return df

#Fetches Technical Indicator
def get_technical_indicator(ticker_symbol, length, indicator):
    df = read_stock_data(ticker_symbol)

    if indicator == 'MA':
        return ti.calculate_simple_moving_average(df, length).dropna()
    elif indicator == 'RSI':
        return ti.calculate_rsi(df, length).dropna()
    elif indicator == 'ROC':
        return ti.calculate_roc(df, length).dropna()
    elif indicator == 'BBP':
        return ti.calculate_bollinger_bands_percent(df, length).dropna()
    else:
        raise ValueError("Unsupported indicator. Please use 'MA','RSI','ROC' or 'BBP'.")

