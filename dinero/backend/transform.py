"""Module for analyzing stock data and fetching relevant news articles."""

from pprint import pprint
import pandas as pd
import numpy as np

from dinero.backend.req import get_news_articles


def find_count_value_change(file : str, value_change: int) -> list:
    """
    Analyzes stock data to find dates with a specified value change percentage.

    Args:
        file (str): Path to the CSV file containing stock data.
        value_change (int): The percentage change value to filter the data by.

    Returns:
        list: A list of dates where the value change percentage meets the criteria.
    """

    stock_data = pd.read_csv(file)

    stock_data['Value Change'] = stock_data['Close'] - stock_data['Open']
    stock_data['Percent Change'] = (stock_data['Value Change']/stock_data['Open'])*100

    if value_change >= 0:
        change_df = stock_data[stock_data['Percent Change']>value_change]
    else:
        change_df = stock_data[stock_data['Percent Change']<value_change]

    return change_df['Date'].to_list()



def get_filter_dates(file_path: str, percent_change: int, stock_ticker : str):
    """
    Fetches news articles related to stock based on percentage value change.

    Args:
        file_path (str): Path to the CSV file containing stock data.
        percent_change (int): The percentage change value to filter the stock data by.
        stock_ticker (str): The ticker symbol of the stock.

    Returns:
        dict: A dictionary where keys are dates with significant value changes, 
              and values are lists of news articles related to the stock on those dates.
    """
    dates_for_articles = find_count_value_change(file_path,percent_change)

    news_articles_links = {}

    for date in dates_for_articles:
        api_response = get_news_articles(stock_ticker,date=date)        
        news_articles_links[date] = [{'content': i['content'], 'title': i['title'], 'link': i['link'], } for i in api_response if any(stock_ticker in symbol for symbol in i['symbols'])]
        
    return news_articles_links