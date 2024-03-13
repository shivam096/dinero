"""
Module: dinero_analysis

This module provides functions for analyzing financial data related to stocks.

Functions:
    - process_dict_to_df: Processes sentiment data from a dictionary to a pandas DataFrame.
    - get_sentiments: Retrieves sentiment analysis for a given stock symbol and percent change.
"""
import os
import pandas as pd
from backend.transform import get_filter_dates
from backend.sentiment_analysis import get_sentiment_value


def process_dict_to_df(sentiment_data):
    """
    Processes sentiment data from a dictionary to a pandas DataFrame.

    Args:
        sentiment_data (dict): A dictionary containing sentiment data for each date.

    Returns:
        pd.DataFrame: A DataFrame containing processed sentiment data.
    """
    data = {
        'Date': [],
        'Title': [],
        'Link': [],
        'Compound Sentiment Score': [],
        'Positive Sentiment Score': [],
        'Negative Sentiment Score': [],
        'Neutral Sentiment Score': []
    }

    for date, articles in sentiment_data.items():
        for title, details in articles.items():
            data['Date'].append(date)
            data['Title'].append(title)
            data['Link'].append(details.get('link', 'N/A'))
            sentiment_score = details.get('sentiment_score', {})
            data['Compound Sentiment Score'].append(sentiment_score.get('compound', 0))
            data['Positive Sentiment Score'].append(sentiment_score.get('pos', 0))
            data['Negative Sentiment Score'].append(sentiment_score.get('neg', 0))
            data['Neutral Sentiment Score'].append(sentiment_score.get('neu', 0))

    formatted_df = pd.DataFrame(data)
    return formatted_df


def get_sentiments(stock_symbol, percent_change):
    """
    Retrieves sentiment analysis for a given stock symbol and percent change.

    Args:
        stock_symbol (str): The stock symbol for which sentiment analysis is to be retrieved.
        percent_change (float): The percent change threshold for filtering dates.

    Returns:
        pd.DataFrame or None: A DataFrame containing sentiment analysis data, 
                            or None if an error occurs.
    """
    sentiment_data = {}
    try:
        if percent_change is None:
            raise ValueError("percent_change argument is None")
        if stock_symbol is None:
            raise ValueError("stock_symbol argument is None")
        file_path = os.path.join("data", f"{stock_symbol}.csv")
        dates_dictionary = get_filter_dates(file_path, percent_change, stock_symbol)

        for key, value in dates_dictionary.items():
            sentiment_data[key] = get_sentiment_value(value)

        data_frame = process_dict_to_df(sentiment_data=sentiment_data)
        return data_frame

    except ValueError as e:
        print(f"Value Error raised: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
