from pprint import pprint
from dinero.backend.req import get_news_articles
from dinero.backend.transform import get_filter_dates


get_filter_dates("dinero/data/AAPL.csv",5, "AAPL")