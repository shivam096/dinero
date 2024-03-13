from pprint import pprint
from backend.sentiment_analysis import get_sentiment_value
from backend.req import get_news_articles
from backend.transform import get_filter_dates
from backend.kpi_manager import get_technical_indicator
import pandas as pd

from backend.processing import get_sentiments

sentiment_date = {}
percent_change = 5
stock_symbol = "AAPL"


print(get_sentiments(stock_symbol,percent_change))


# data = {
#     'Date': [],
#     'Title': [],
#     'Link': [],
#     'Compound Sentiment Score': [],
#     'Positive Sentiment Score': [],
#     'Negative Sentiment Score': [],
#     'Neutral Sentiment Score': []
# }

# for date, articles in sentiment_date.items():
#     for title, details in articles.items():
#         data['Date'].append(date)
#         data['Title'].append(title)
#         data['Link'].append(details['link'])
#         data['Compound Sentiment Score'].append(details['sentiment_score']['compound'])
#         data['Positive Sentiment Score'].append(details['sentiment_score']['pos'])
#         data['Negative Sentiment Score'].append(details['sentiment_score']['neg'])
#         data['Neutral Sentiment Score'].append(details['sentiment_score']['neu'])

# df = pd.DataFrame(data)
# print(df)




# # usage of KPI
# ticker_symbol = 'AAPL'
# length = 50
# indicator = 'MA'

# indicator_data = get_technical_indicator(ticker_symbol, length, indicator)
# print(indicator_data)
