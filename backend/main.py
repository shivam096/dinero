from pprint import pprint
from sentiment_analysis import get_sentiment_value
from req import get_news_articles
from transform import get_filter_dates
from kpi_manager import get_technical_indicator

sentiment_date = {}

dates_dictionary = get_filter_dates("data/AAPL.csv",5, "AAPL")


pprint(dates_dictionary)


for key,value in dates_dictionary.items():
    
    sentiment_date[key] = get_sentiment_value(value)
    
pprint(sentiment_date)

# usage of KPI
ticker_symbol = 'AAPL'
length = 50
indicator = 'MA'

indicator_data = get_technical_indicator(ticker_symbol, length, indicator)
pprint(indicator_data)
