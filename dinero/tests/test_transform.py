"""
This module contains unit tests for the stock analysis functions in backend.transform module.
"""

import unittest
from unittest.mock import patch
import pandas as pd

from backend.transform import find_count_value_change, get_filter_dates

class TestStockAnalysis(unittest.TestCase):
    """
    A class containing unit tests for stock analysis functions.
    """

    @patch('backend.transform.pd.read_csv')
    def test_find_count_value_change(self, mock_read_csv):
        """
        Test the find_count_value_change function.

        Parameters:
        - mock_read_csv (MagicMock): A mock object for pd.read_csv.

        Returns:
        None
        """
        # Mocking CSV file reading
        mock_data = {
            'Date': ['2024-03-01', '2024-03-02', '2024-03-03'],
            'Open': [100, 110, 120],
            'Close': [120, 100, 125]
        }
        mock_read_csv.return_value = pd.DataFrame(mock_data)

        # Test with positive value_change
        result_positive = find_count_value_change('../data/AAPL.csv', 5)
        self.assertEqual(result_positive, ['2024-03-01'])

        # Test with negative value_change
        result_negative = find_count_value_change(
            '../data/AAPL.csv', -5)
        self.assertEqual(result_negative, ['2024-03-02'])

    @patch('backend.transform.pd.read_csv')
    @patch('backend.transform.get_news_articles')
    def test_get_filter_dates(self, mock_get_news_articles, mock_read_csv):
        """
        Test the get_filter_dates function.

        Parameters:
        - mock_get_news_articles (MagicMock): A mock object for get_news_articles.
        - mock_read_csv (MagicMock): A mock object for pd.read_csv.

        Returns:
        None
        """
        # Mocking news articles fetching
        mock_get_news_articles.side_effect = [
            [{'content': 'Content 1', 'title': 'Title 1', 'link': 'Link 1', 'symbols': ['AAPL']}],
            [{'content': 'Content 2', 'title': 'Title 2', 'link': 'Link 2', 'symbols': ['XYZ']}],
            [{'content': 'Content 3', 'title': 'Title 3', 'link': 'Link 3',
              'symbols': ['AAPL', 'XYZ']}]
        ]
        mock_data = {
            'Date': ['2024-03-01', '2024-03-02', '2024-03-03'],
            'Open': [100, 110, 120],
            'Close': [120, 100, 125]
        }
        mock_read_csv.return_value = pd.DataFrame(mock_data)

        # Test with mock data and stock_ticker 'ABC'
        result_aapl= get_filter_dates(
            '../data/AAPL.csv', 10, 'AAPL')
        expected_result_aapl = {'2024-03-01': [{'content': 'Content 1',
                                                'link': 'Link 1', 
                                                'title': 'Title 1'}]}
        self.assertDictEqual(result_aapl, expected_result_aapl)

        # Test with mock data and stock_ticker 'XYZ'
        result_aapl = get_filter_dates(
            '../data/AAPL.csv', 5, 'AAPL')
        expected_result_aapl ={'2024-03-01': []}
        self.assertDictEqual(result_aapl, expected_result_aapl)

if __name__ == '__main__':
    unittest.main()
