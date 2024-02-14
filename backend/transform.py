from pprint import pprint
import pandas as pd
import numpy as np

from req import get_news_articles


def find_count_value_change(file : str, value_change: int) -> list:
    
    stock_data = pd.read_csv(file)
    
    stock_data['Value Change'] = stock_data['Close'] - stock_data['Open']
    stock_data['Percent Change'] = (stock_data['Value Change']/stock_data['Open'])*100
    
    if value_change >= 0:
        change_df = stock_data[stock_data['Percent Change']>value_change]
    else:
        change_df = stock_data[stock_data['Percent Change']<value_change]
    
    return change_df['Date'].to_list()



def get_filter_dates(file_path: str, percent_change: int, stock_ticker : str):
    dates_for_articles = find_count_value_change(file_path,percent_change)

    news_articles_links = {}

    for date in dates_for_articles:
        api_response = get_news_articles(stock_ticker,date=date)
        
        news_articles_links[date] = [i['title'] for i in api_response if any(stock_ticker in symbol for symbol in i['symbols'])]
        
    return news_articles_links