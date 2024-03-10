from pprint import pprint
from backend.sentiment_analysis import get_sentiment_value
from backend.req import get_news_articles
from backend.transform import get_filter_dates
from backend.kpi_manager import get_technical_indicator

sentiment_date = {}
stock_symbol = "AAPL"
file_path = f"dinero/data/{stock_symbol}.csv"
percent_change = 5

dates_dictionary = get_filter_dates(file_path, percent_change, stock_symbol)


pprint(dates_dictionary)


for key,value in dates_dictionary.items():

    sentiment_date[key] = get_sentiment_value(value)

pprint(sentiment_date)

# usage of KPI
ticker_symbol = 'AAPL'
length = 50
indicator = 'MA'

indicator_data = get_technical_indicator(ticker_symbol, length, indicator)
print(indicator_data)
