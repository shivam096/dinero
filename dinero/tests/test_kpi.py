"""Unit tests for the KPI (Key Performance Indicators) Manager module.

This module contains unittests for testing the functionality of the KPI Manager, particularly focusing on reading stock data and calculating various technical indicators.
"""
import unittest
from unittest.mock import patch
import pandas as pd
from backend.kpi_manager import get_technical_indicator, read_stock_data


class TestKPIManager(unittest.TestCase):
    """Tests for KPI manager and Technical indicators"""

    @patch("pandas.read_csv")
    def test_read_stock_data(self, mock_read_csv):
        """Test reading stock data from a CSV file, simulating a successful file read."""
        mock_read_csv.return_value = pd.DataFrame({"Close": [100, 200, 300]})
        df = read_stock_data("AAPL")
        mock_read_csv.assert_called_once_with("dinero/data/AAPL.csv")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)

    @patch("backend.kpi_manager.read_stock_data")
    @patch("backend.technical_indicators.calculate_simple_moving_average")
    def test_get_technical_indicator_ma(self, mock_ma, mock_read_stock):
        """Test retrieval of the moving average indicator using mocked stock data."""
        mock_df = pd.DataFrame({"Close": [100, 200, 300]})
        mock_read_stock.return_value = mock_df
        mock_ma.return_value = pd.Series([100, 110, 120])

        result = get_technical_indicator("AAPL", 10, "MA")
        mock_ma.assert_called_once_with(mock_df, 10)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(list(result), [100, 110, 120])

    @patch("backend.kpi_manager.read_stock_data")
    @patch("backend.technical_indicators.calculate_rsi")
    def test_get_technical_indicator_rsi(self, mock_rsi, mock_read_stock):
        """Test retrieval of the RSI indicator with mocked stock data and RSI calculation."""
        mock_df = pd.DataFrame({"Close": [100, 200, 300]})
        mock_read_stock.return_value = mock_df
        mock_rsi.return_value = pd.Series([30, 50, 70])

        result = get_technical_indicator("AAPL", 14, "RSI")
        mock_rsi.assert_called_once_with(mock_df, 14)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(list(result), [30, 50, 70])

    @patch("backend.kpi_manager.read_stock_data")
    @patch("backend.technical_indicators.calculate_roc")
    def test_get_technical_indicator_roc(self, mock_roc, mock_read_stock):
        """Test retrieval of the ROC indicator ensuring proper interaction with mocks."""
        mock_df = pd.DataFrame({"Close": [100, 200, 300]})
        mock_read_stock.return_value = mock_df
        mock_roc.return_value = pd.Series([10, 20, 30])

        result = get_technical_indicator("AAPL", 10, "ROC")
        mock_roc.assert_called_once_with(mock_df, 10)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(list(result), [10, 20, 30])

    @patch("backend.kpi_manager.read_stock_data")
    @patch("backend.technical_indicators.calculate_bollinger_bands_percent")
    def test_get_technical_indicator_bbp(self, mock_bbp, mock_read_stock):
        """Test the Bollinger Bands Percent indicator function with mocked dependencies."""
        mock_df = pd.DataFrame({"Close": [100, 200, 300]})
        mock_read_stock.return_value = mock_df
        mock_bbp.return_value = pd.Series([0.1, 0.5, 0.9])

        result = get_technical_indicator("AAPL", 20, "BBP")
        mock_bbp.assert_called_once_with(mock_df, 20)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(list(result), [0.1, 0.5, 0.9])

    def test_get_technical_indicator_unsupported(self):
        """Ensure that an unsupported indicator type raises a ValueError."""
        with self.assertRaises(ValueError):
            get_technical_indicator("AAPL", 10, "UNKNOWN")

    def test_read_stock_data_file_not_found(self):
        """Test the file not found error handling in reading stock data from a CSV file."""
        with self.assertRaises(FileNotFoundError):
            read_stock_data('NON_EXISTENT_SYMBOL')


# This allows the test suite to be run from the command line
if __name__ == "__main__":
    unittest.main()
