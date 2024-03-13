"""
    test_sentiment_analysis.py
===========

This module contains unit tests for the request module

Classes:
    TestGetNewsArticles: Test cases for the module.
"""
import unittest
from backend.sentiment_analysis import get_sentiment_value

class TestSentimentAnalysis(unittest.TestCase):
    """Test case for sentiment analysis module."""
    def setUp(self):
        """Set up test data."""
        self.titles = [
            {'title': 'Positive title',
             'content': 'This is a great day!',
             'link': 'http://example.com/positive'},
            {'title': 'Negative title',
             'content': 'I feel terrible.',
             'link': 'http://example.com/negative'},
            {'title': 'Neutral title',
             'content': 'The weather is okay.',
             'link': 'http://example.com/neutral'}
        ]

    def test_sentiment_analysis(self):
        """Test sentiment analysis function."""
        expected_result = {
            'Positive title': {'sentiment_score':
                {'neg': 0.0, 'neu': 0.406, 'pos': 0.594, 'compound': 0.6588},
                'link': 'http://example.com/positive'},
            'Negative title': {'sentiment_score':
                {'neg': 0.756, 'neu': 0.244, 'pos': 0.0, 'compound': -0.4767},
                               'link': 'http://example.com/negative'},
            'Neutral title': {'sentiment_score':
                {'neg': 0.0, 'neu': 0.612, 'pos': 0.388, 'compound': 0.2263},
                'link': 'http://example.com/neutral'}
        }
        result = get_sentiment_value(self.titles)

        self.assertEqual(result, expected_result)

    def test_empty_input(self):
        """Test behavior with empty input."""
        result = get_sentiment_value([])
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
