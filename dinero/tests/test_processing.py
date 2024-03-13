"""
test_processing.py
===========

This module contains unit tests for the processing module

Classes:
    TestDineroAnalysis: Test cases for the processing module.
"""
import unittest
import pandas as pd
from backend.processing import process_dict_to_df, get_sentiments

class TestDineroAnalysis(unittest.TestCase):
    """
    Test cases for the dinero_analysis module functions.
    """
    def setUp(self):
        """
        Set up any data or variables needed for the test cases.
        """
        self.sentiment_data = {
            '2024-01-01': {
                'Article 1': {'link': 'link1', 'sentiment_score':
                    {'compound': 0.5, 'pos': 0.3, 'neg': 0.1, 'neu': 0.6}},
                'Article 2': {'link': 'link2', 'sentiment_score':
                    {'compound': -0.2, 'pos': 0.1, 'neg': 0.4, 'neu': 0.5}}
            },
            '2024-01-02': {
                'Article 3': {'link': 'link3', 'sentiment_score':
                    {'compound': 0.8, 'pos': 0.6, 'neg': 0.0, 'neu': 0.4}},
                'Article 4': {'link': 'link4', 'sentiment_score':
                    {'compound': -0.5, 'pos': 0.2, 'neg': 0.6, 'neu': 0.2}}
            }
        }

    def test_process_dict_to_df(self):
        """
        Test the process_dict_to_df function.
        """
        expected_columns = ['Date', 'Title', 'Link', 'Compound Sentiment Score',
                            'Positive Sentiment Score', 'Negative Sentiment Score',
                            'Neutral Sentiment Score']
        df = process_dict_to_df(self.sentiment_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertCountEqual(df.columns.tolist(), expected_columns)
        self.assertEqual(len(df), 4)  # Check if all articles are processed

    def test_get_sentiments(self):
        """
        Test the get_sentiments function with valid and invalid inputs.
        """
        # Test the get_sentiments function with valid inputs
        df = get_sentiments('AAPL', 2.0)  # Example valid stock symbol and percent change
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)  # Check if DataFrame is not empty

        # Test the get_sentiments function with None inputs
        df_none_symbol = get_sentiments(None, 2.0)
        df_none_change = get_sentiments('AAPL', None)
        self.assertIsNone(df_none_symbol)  # Check if None stock symbol returns None
        self.assertIsNone(df_none_change)  # Check if None percent change returns None

if __name__ == '__main__':
    unittest.main()
