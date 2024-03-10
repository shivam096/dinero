import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from dinero.backend.transform import find_count_value_change, get_filter_dates

class TestStockAnalysis(unittest.TestCase):

    @patch('dinero.backend.transform.pd.read_csv')
    def test_find_count_value_change(self, mock_read_csv):
        # Mocking CSV file reading
        mock_data = {
            'Date': ['2024-03-01', '2024-03-02', '2024-03-03'],
            'Open': [100, 110, 120],
            'Close': [120, 100, 125]
        }
        mock_read_csv.return_value = pd.DataFrame(mock_data)

        # Test with positive value_change
        result_positive = find_count_value_change('/Users/stlp/Documents/data557/final_project/new_pull/dinero/dinero/data/AAPL.csv', 5)
        self.assertEqual(result_positive, ['2024-03-01'])

        # Test with negative value_change
        result_negative = find_count_value_change('/Users/stlp/Documents/data557/final_project/new_pull/dinero/dinero/data/AAPL.csv', -5)
        self.assertEqual(result_negative, ['2024-03-02'])

    @patch('dinero.backend.transform.pd.read_csv')
    @patch('dinero.backend.transform.get_news_articles')
    def test_get_filter_dates(self, mock_get_news_articles, mock_read_csv):
        # Mocking news articles fetching
        mock_get_news_articles.side_effect = [
            [{'content': 'Content 1', 'title': 'Title 1', 'link': 'Link 1', 'symbols': ['AAPL']}],
            [{'content': 'Content 2', 'title': 'Title 2', 'link': 'Link 2', 'symbols': ['XYZ']}],
            [{'content': 'Content 3', 'title': 'Title 3', 'link': 'Link 3', 'symbols': ['AAPL', 'XYZ']}]
        ]
        
        mock_data = {
            'Date': ['2024-03-01', '2024-03-02', '2024-03-03'],
            'Open': [100, 110, 120],
            'Close': [120, 100, 125]
        }
        mock_read_csv.return_value = pd.DataFrame(mock_data)
        
        # Test with mock data and stock_ticker 'ABC'
        result_ABC = get_filter_dates('/Users/stlp/Documents/data557/final_project/new_pull/dinero/dinero/data/AAPL.csv', 10, 'AAPL')
        print(result_ABC)
        expected_result_ABC = {'2024-03-01': [{'content': 'Content 1', 'link': 'Link 1', 'title': 'Title 1'}]}
        self.assertDictEqual(result_ABC, expected_result_ABC)

        # Test with mock data and stock_ticker 'XYZ'
        result_XYZ = get_filter_dates('/Users/stlp/Documents/data557/final_project/new_pull/dinero/dinero/data/AAPL.csv', 5, 'AAPL')
        expected_result_XYZ ={'2024-03-01': []}
        self.assertDictEqual(result_XYZ, expected_result_XYZ)

if __name__ == '__main__':
    unittest.main()
