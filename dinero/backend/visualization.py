"""
visualization.py
=================
This module creates and controls interactive plots using plotly package.

Functions:
    1. plot_stock_price(ticker_symbol)
    2. plot_kpis(stock_fig, ticker_symbol, length, kpi_name)
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from backend.stock_data_manager import get_stock_data
from backend.kpi_manager import get_technical_indicator

def plot_stock_price(ticker_symbol):
    """
    Plot a candlestick chart for the given stock ticker symbol.

    Parameters:
    ticker_symbol (str): The ticker symbol of the stock.

    Returns:
    plotly.graph_objects.Figure:
    The price of teh given stock ticker in candlestick chart with features:
        customized titles
        tooltip with price info
        allow view adjustment through xrange slider
        allow view adjustment through time buttons
    """
    stock_data = get_stock_data(ticker_symbol)

    fig_candlestick = go.Figure()
    fig_candlestick.add_trace(go.Candlestick(x=stock_data['Date'],
                                            open=stock_data['Open'],
                                            high=stock_data['High'],
                                            low=stock_data['Low'],
                                            close=stock_data['Close'],
                                            name='Candlestick'))

    # Update layout for candlestick chart
    fig_candlestick.update_layout(title=f'Candlestick Chart',
                                xaxis_title="Date", yaxis_title="Price")
    fig_candlestick.update_layout(hovermode="x unified")
    time_buttons = [
        {'step': 'all', 'label': 'All'},
        {'count': 3, 'step': 'year', 'stepmode': 'backward', 'label': '3 Year'},
        {'count': 1, 'step': 'year', 'stepmode': 'backward', 'label': '1 Year'},
        {'count': 6, 'step': 'month', 'stepmode': 'backward', 'label': '6 Month'},
        {'count': 1, 'step': 'month', 'stepmode': 'backward', 'label': '1 Month'},
        {'count': 1, 'step': 'year', 'stepmode': 'todate', 'label': '1 Year To Date'}
    ]
    fig_candlestick.update_xaxes(rangeselector={'buttons': time_buttons})
    fig_candlestick.update_yaxes(autorange=True, fixedrange = False)

    return fig_candlestick

def plot_kpis(stock_fig, ticker_symbol, length, kpi_name):
    """
    Plot the specified technical indicator for the given stock.

    Parameters:
    stock_fig (plotly.graph_objects.Figure):
        The Plotly figure object representing the stock chart.
    ticker_symbol (str):
        The ticker symbol of the stock.
    length (int):
        The length of timeframe (in days) to calculate corresponding indicator.
    indicator_name (str):
        The name of the technical indicator to plot.

    Returns:
    None if plot of 'MA' indicator, plotly.graph_objects.Figure otherwise.

    The Plotly figure object (if returned) contains two subplots：
        - the stock prie
        - the technical indicator
    with features:
        customized color and titles
        tooltip with technical indicator value
        allow view adjustment through xrange slider

    Side Effects if None returned:
    Modify the features of given stock_fig:
        add trace of technical indicator
        customize color and titles
        integrate tooltip
        add legend
    """
    indicator = get_technical_indicator(ticker_symbol,int(length),kpi_name)

    if kpi_name == 'MA':
        stock_fig.add_trace(go.Scatter(x=indicator['Date'], y=indicator[indicator.columns[1]],
                                       mode='lines', name=indicator.columns[1]))
        stock_fig.update_layout(title=f'{ticker_symbol} Stock Candlestick Chart with {kpi_name}')
        candles = stock_fig.data[0]
        candles.increasing.fillcolor = '#3D9970' # green
        candles.increasing.line.color = '#3D9970'
        candles.decreasing.fillcolor = '#FF4136' # red
        candles.decreasing.line.color = '#FF4136'
        return None

    kpi_fig = make_subplots(rows=2, cols=1)

    stock_data = get_stock_data(ticker_symbol)
    kpi_fig.add_trace(go.Scatter(x=indicator['Date'], y=stock_data['Close'],
                                 mode='lines', name='Close Price'), row=1, col=1)
    kpi_fig.add_trace(go.Scatter(x=indicator['Date'], y=indicator[indicator.columns[1]],
                                 mode='lines', name=kpi_name), row=2, col=1)

    # Update layout for the KPI line chart
    kpi_fig.update_layout(hovermode="x unified")
    kpi_fig.update_traces(xaxis='x1')
    kpi_fig.update_layout(title=f'{kpi_name} for {ticker_symbol}',
                          xaxis_title="Date", yaxis_title="Price")

    time_buttons = [
        {'step': 'all', 'label': 'All'},
        {'count': 3, 'step': 'year', 'stepmode': 'backward', 'label': '3 Year'},
        {'count': 1, 'step': 'year', 'stepmode': 'backward', 'label': '1 Year'},
        {'count': 6, 'step': 'month', 'stepmode': 'backward', 'label': '6 Month'},
        {'count': 1, 'step': 'month', 'stepmode': 'backward', 'label': '1 Month'},
        {'count': 1, 'step': 'year', 'stepmode': 'todate', 'label': '1 Year To Date'}
    ]
    kpi_fig.update_xaxes(rangeselector={'buttons': time_buttons})
    kpi_fig.update_yaxes(autorange=True, fixedrange = False)
    return kpi_fig
