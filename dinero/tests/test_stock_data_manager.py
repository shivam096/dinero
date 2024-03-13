"""
test_stock_data_manager.py
===========

This module contains unit tests for the stock_data_manager module.

Classes:
    TestStockDataManager: Test cases for the stock_data_manager module.
"""

import unittest
from unittest import mock
import os
from datetime import datetime
import pandas as pd

from backend.stock_data_manager import (
    download_stock_data,
    update_stock_data,
    get_stock_data,
    get_filtered_stock_data,
    get_last_n_days,
    DEFAULT_DATABASE_PATH
)

class TestStockDataManager(unittest.TestCase):
    """
    Test cases for the stock_data_manager module:
    Test non-trivial functions in dinero/backend/stock_data_manager.py:
        1. download_stock_data(ticker_symbol, period_str='5y')
        3. update_stock_data()
        4. get_stock_data(ticker_symbol)
        5. get_filtered_stock_data(ticker_symbol, start_date='', end_date='')
        6. get_last_n_days(stock_data, n_days)

    Notes:
    2.`get_existing_tickers` is TRIVIAL and is called by update_stock_data(),
    so it has no explicit testing.
    """

    @mock.patch('backend.stock_data_manager.yf.download')
    def test_default_download_stock_data(self, mock_download):
        """
        Test download with (valid) default period
        (using mock to simulate yfinance download)
        """
        mock_download.return_value = pd.DataFrame({"Close": [100, 200, 300]})
        num = download_stock_data('test_ticker')
        self.assertIsInstance(num, int)
        file_path = f'{DEFAULT_DATABASE_PATH}/TEST_TICKER.csv'
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

    @mock.patch('backend.stock_data_manager.yf.download')
    def test_download_stock_data_invalid_input_type(self, mock_download):
        """
        Test download with invalid input type
        (using mock to simulate yfinance download)
        """
        mock_download.return_value = pd.DataFrame({"Close": [100, 200, 300]})
        with self.assertRaises(TypeError):
            download_stock_data('test_ticker', 1)
        file_path = f'{DEFAULT_DATABASE_PATH}/TEST_TICKER.csv'
        self.assertFalse(os.path.exists(file_path))

    @mock.patch('backend.stock_data_manager.yf.download')
    def test_download_stock_data_invalid_period(self, mock_download):
        """
        Test download with invalid period input
        (using mock to simulate yfinance download)
        """
        mock_download.return_value = pd.DataFrame({"Close": [100, 200, 300]})
        with self.assertRaises(ValueError):
            download_stock_data('test_ticker', '1')
        file_path = f'{DEFAULT_DATABASE_PATH}/TEST_TICKER.csv'
        self.assertFalse(os.path.exists(file_path))

    @mock.patch('backend.stock_data_manager.yf.download')
    def test_download_stock_data_invalid_ticker(self, mock_download):
        """
        Test download with invalid ticker input
        (using mock to simulate yfinance download)
        """
        mock_download.return_value = pd.DataFrame()
        with self.assertRaises(ValueError):
            download_stock_data('invalid', '1d')
        file_path = f'{DEFAULT_DATABASE_PATH}/INVALID.csv'
        self.assertFalse(os.path.exists(file_path))

    @mock.patch('backend.stock_data_manager.yf.download')
    def test_update_stock_data(self, mock_download):
        """
        Test update stock database
        (using mock to simulate yfinance download)
        """
        mock_download.return_value = pd.DataFrame()
        tickers = update_stock_data()
        self.assertIsInstance(tickers, list)
        for ticker in tickers:
            file_path = f'{DEFAULT_DATABASE_PATH}/{ticker}.csv'
            self.assertTrue(os.path.exists(file_path))

    @mock.patch("backend.stock_data_manager.pd.read_csv")
    def test_get_stock_data(self, mock_read_csv):
        """
        Test fetch stock data from database
        (using mock to simulate a successful file read)
        """
        mock_read_csv.return_value = pd.DataFrame({"Close": [100, 200, 300]})
        data = get_stock_data('MSFT')
        mock_read_csv.assert_called_once_with(os.path.join("data","MSFT.csv"))
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 3)

    def test_get_stock_data_invalid_ticker(self):
        """
        Test fetch non-existing stock data from database
        """
        with self.assertRaises(TypeError):
            get_stock_data(1)
        with self.assertRaises(ValueError):
            get_stock_data('NON_EXISTENT_SYMBOL')

    def test_default_get_filtered_stock_data(self):
        """
        Test fetch filtered stock data from database with defult inputs
        """
        data = get_filtered_stock_data('MSFT')
        expected_data = get_stock_data('MSFT')
        self.assertTrue(data.equals(expected_data))

    def test_get_filtered_stock_data_with_valid_input(self):
        """
        Test fetch filtered stock data from database with valid input
        """
        test_date = datetime.today().strftime('%Y-%m-%d')
        data = get_filtered_stock_data('MSFT', test_date, test_date)
        self.assertIsInstance(data, pd.DataFrame)

    def test_get_filtered_stock_data_with_invalid_input(self):
        """
        Test fetch filtered stock data from database with invalid input
        """
        with self.assertRaises(TypeError):
            get_filtered_stock_data('MSFT', 20240101, '2023/01/0')
        with self.assertRaises(ValueError):
            get_filtered_stock_data('MSFT', '2024/01/01', '2023/01/0')

    def test_get_last_n_days_valid(self):
        """
        Test get data of n last days from dataframe with valid input
        (num of days > len(dataframe))
        """
        test_df = pd.DataFrame({"Date": ['2023/01/0', '2023/10/01',
                                         '2024/11/01','2024/01/01']})
        test_result = get_last_n_days(test_df,6)
        self.assertIsInstance(test_result, pd.DataFrame)
        self.assertEqual(len(test_result), 4)

    def test_get_last_n_days_invalid(self):
        """
        Test get data of n last days from dataframe with invalid input
        """
        test_df = pd.DataFrame({"Date": ['2023/01/0', '2023/10/01',
                                         '2024/11/01','2024/01/01']})
        with self.assertRaises(TypeError):
            get_last_n_days(['2023/01/0'],2)
        with self.assertRaises(TypeError):
            get_last_n_days(test_df,"1")
        with self.assertRaises(ValueError):
            get_last_n_days(test_df,-1)

if __name__ == '__main__':
    unittest.main()
