"""
test_visualization.py
===========

This module contains unit tests for the visualization module.

Classes:
    TestVisualization: Test cases for the visualization module.
"""

import unittest
import plotly.graph_objects as go

from backend.visualization import (
    plot_stock_price,
    plot_kpis
)

class TestVisualization(unittest.TestCase):
    """
    Test cases for functions in the visualization module:
        1. plot_stock_price(ticker_symbol)
        2. plot_kpis(stock_fig, ticker_symbol, length, kpi_name)
    """

    def test_plot_stock_price_layout(self):
        """
        Test the layout of the stock price candlestick chart.

        Checks if the layout of the candlestick chart is as expected.
        """
        stock_price_fig = plot_stock_price('MSFT')
        self.assertIsInstance(stock_price_fig, go.Figure)
        self.assertEqual(len(stock_price_fig.data), 1)
        self.assertEqual(stock_price_fig.data[0].type, 'candlestick')
        self.assertEqual(stock_price_fig.layout.hovermode, 'x unified')
        self.assertEqual(stock_price_fig.layout.title['text'],
                         'Candlestick Chart')
        self.assertEqual(stock_price_fig.layout.xaxis.title['text'], 'Date')
        self.assertEqual(stock_price_fig.layout.yaxis.title['text'], 'Price')

    def test_plot_stock_price_selector_view_adjustment(self):
        """
        Test the adjustment of time range selector buttons and y-axis
        range in the stock price chart.

        Checks if the time range selector buttons are correctly added
        and if y-axis range is set to auto.
        """
        stock_price_fig = plot_stock_price('MSFT')
        time_buttons = [
        {'step': 'all', 'label': 'All'},
        {'count': 3, 'step': 'year', 'stepmode': 'backward', 'label': '3 Year'},
        {'count': 1, 'step': 'year', 'stepmode': 'backward', 'label': '1 Year'},
        {'count': 6, 'step': 'month', 'stepmode': 'backward', 'label': '6 Month'},
        {'count': 1, 'step': 'month', 'stepmode': 'backward', 'label': '1 Month'},
        {'count': 1, 'step': 'year', 'stepmode': 'todate', 'label': '1 Year To Date'}
        ]
        self.assertEqual(len(stock_price_fig.layout.xaxis.rangeselector.buttons),
                        len(time_buttons))
        self.assertTrue(stock_price_fig.layout.yaxis.autorange)
        self.assertFalse(stock_price_fig.layout.yaxis.fixedrange)

    def test_plot_kpi_ma(self):
        """
        Test plotting Moving Average (MA) on the stock price chart.

        Checks if Moving Average is correctly added to the stock price candlestick chart.
        """
        stock_price_fig = plot_stock_price('MSFT')
        kpi_fig = plot_kpis(stock_price_fig, 'MSFT', 50, 'MA')
        self.assertIsNone(kpi_fig)
        self.assertEqual(stock_price_fig.layout.title['text'],
                         'MSFT Stock Candlestick Chart with MA')
        self.assertEqual(len(stock_price_fig.data), 2)
        self.assertEqual(stock_price_fig.data[1].type, 'scatter')

    def test_plot_kpi_other(self):
        """
        Test plotting other technical indicators on the stock price chart.

        Checks if other technical indicators are correctly added to
        the stock price candlestick chart.
        """
        stock_price_fig = plot_stock_price('MSFT')
        kpi_fig = plot_kpis(stock_price_fig, 'MSFT', 50, 'ROC')
        self.assertIsInstance(kpi_fig, go.Figure)
        self.assertEqual(kpi_fig.layout.title['text'],
                         'ROC for MSFT')
        self.assertEqual(len(kpi_fig.data), 2)
        self.assertEqual(kpi_fig.data[0].type, 'scatter')
        self.assertEqual(kpi_fig.data[0].name, 'Close Price')
        self.assertEqual(kpi_fig.data[1].type, 'scatter')
        self.assertEqual(kpi_fig.data[1].name, 'ROC')

if __name__ == '__main__':
    unittest.main()
