from pprint import pprint
from sentiment_analysis import get_sentiment_value
from req import get_news_articles
from transform import get_filter_dates
from kpi_manager import get_technical_indicator

sentiment_date = {}
stock_symbol = "AAPL"
file_path = os.path.join("data", f'{stock_symbol}.csv')
dates_dictionary = get_filter_dates(file_path,5, stock_ticker)


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
