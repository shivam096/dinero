"""
    test-req.py
===========

This module contains unit tests for the request module

Classes:
    TestGetNewsArticles: Test cases for the module.
"""
import unittest
from unittest.mock import patch
from backend.req import get_news_articles

class TestGetNewsArticles(unittest.TestCase):
    """Test case for the get_news_articles function."""

    @patch('backend.req.requests.get')
    def test_get_news_articles_success(self, mock_get):
        """Test get_news_articles function for successful API response."""
        # Arrange
        mock_response = {
            "status": "success",
            "articles": [
                {"title": "Article 1", "content": "Content 1"},
                {"title": "Article 2", "content": "Content 2"}
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        ticker = 'AAPL'
        date = '2024-03-09'

        # Act
        result = get_news_articles(ticker, date)

        # Assert
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['articles']), 2)
        self.assertEqual(result['articles'][0]['title'], 'Article 1')
        self.assertEqual(result['articles'][0]['content'], 'Content 1')
        self.assertEqual(result['articles'][1]['title'], 'Article 2')
        self.assertEqual(result['articles'][1]['content'], 'Content 2')

    @patch('backend.req.requests.get')
    def test_get_news_articles_api_failure(self, mock_get):
        """Test get_news_articles function for API failure response."""
        # Arrange
        mock_response = {"status": "error", "message": "API error"}
        mock_get.return_value.json.return_value = mock_response
        ticker = 'AAPL'
        date = '2024-03-09'

        # Act
        result = get_news_articles(ticker, date)

        # Assert
        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['message'], 'API error')

if __name__ == '__main__':
    unittest.main()
