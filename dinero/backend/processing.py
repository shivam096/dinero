"""
Module: dinero_analysis

This module provides functions for analyzing financial data related to stocks.

Functions:
    - get_filter_dates: Retrieves and filters financial data for a specified stock within a specified date range.
"""

from pprint import pprint
from dinero.backend.req import get_news_articles
from dinero.backend.transform import get_filter_dates


get_filter_dates("dinero/data/AAPL.csv",5, "AAPL")