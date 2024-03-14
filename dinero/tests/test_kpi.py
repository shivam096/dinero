"""Unit tests for the KPI (Key Performance Indicators) Manager module.

This module contains unittests for testing the functionality of the KPI Manager, particularly
focusing on reading stock data and calculating various technical indicators.
"""
import unittest
from unittest.mock import patch
import pandas as pd
from backend.technical_indicators import _formatted_dataframe
from backend.kpi_manager import get_technical_indicator

class TestKPIManager(unittest.TestCase):
    """Tests for KPI manager and Technical indicators"""

    @patch("backend.kpi_manager.get_stock_data")
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

    @patch("backend.kpi_manager.get_stock_data")
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

    @patch("backend.kpi_manager.get_stock_data")
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

    @patch("backend.kpi_manager.get_stock_data")
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

    def test_formatted_dataframe(self):
        """Test the _formatted_dataframe function to ensure it formats the DataFrame correctly."""
        mock_data = pd.DataFrame({
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'Dummy': [1, 2, 3]  # This column won't be used, just to simulate structure
        })
        mock_indicator = pd.Series([0.1, 0.5, 0.9], name='BBP')
        result_df = _formatted_dataframe(mock_data, mock_indicator, 'BBP')

        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertListEqual(list(result_df['Date']), list(mock_data['Date']))

    def test_formatted_dataframe_with_invalid_data_type(self):
        """Test _formatted_dataframe with invalid data type for data parameter."""
        mock_data = "not a dataframe"
        mock_indicator = pd.Series([1, 2, 3])
        with self.assertRaises(TypeError) as context:
            _formatted_dataframe(mock_data, mock_indicator, 'TestName')
        self.assertTrue("data must be a pandas DataFrame" in str(context.exception))

    def test_formatted_dataframe_with_invalid_name_type(self):
        """Test _formatted_dataframe with invalid data type for name parameter."""
        mock_data = pd.DataFrame({'Date': ['2023-01-01', '2023-01-02'], 'Close': [100, 200]})
        mock_indicator = pd.Series([1, 2])
        with self.assertRaises(TypeError) as context:
            _formatted_dataframe(mock_data, mock_indicator, 123)
        self.assertTrue("name must be a string" in str(context.exception))


# This allows the test suite to be run from the command line
if __name__ == "__main__":
    unittest.main()
