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