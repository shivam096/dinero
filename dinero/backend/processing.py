"""
Module: dinero_analysis

This module provides functions for analyzing financial data related to stocks.

Functions:
    - process_dict_to_df
    - get_sentiments
"""

import os
import pandas as pd
from pprint import pprint
from backend.transform import get_filter_dates
from backend.sentiment_analysis import get_sentiment_value


def process_dict_to_df(sentiment_data):
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
            data['Link'].append(details['link'])
            data['Compound Sentiment Score'].append(details['sentiment_score']['compound'])
            data['Positive Sentiment Score'].append(details['sentiment_score']['pos'])
            data['Negative Sentiment Score'].append(details['sentiment_score']['neg'])
            data['Neutral Sentiment Score'].append(details['sentiment_score']['neu'])

    formatted_df = pd.DataFrame(data)
    return formatted_df


def get_sentiments(stock_symbol,percent_change):
    sentiment_data ={}
    file_path = os.path.join("data",f"{stock_symbol}.csv")
    dates_dictionary = get_filter_dates(file_path, percent_change, stock_symbol)

    for key,value in dates_dictionary.items():
        sentiment_data[key] = get_sentiment_value(value)

    data_frame = process_dict_to_df(sentiment_data=sentiment_data)
    return data_frame
