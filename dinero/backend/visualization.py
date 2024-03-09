import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from backend.data_manager import get_stock_data
from backend.kpi_manager import get_technical_indicator


def plot_stock_price(ticker_symbol):
    stock_data = get_stock_data(ticker_symbol)

    fig_candlestick = go.Figure()
    fig_candlestick.add_trace(go.Candlestick(x=stock_data['Date'],
                                            open=stock_data['Open'],
                                            high=stock_data['High'],
                                            low=stock_data['Low'],
                                            close=stock_data['Close'],
                                            name='Candlestick'))

    # Update layout for candlestick chart
    fig_candlestick.update_layout(xaxis_title="Date", yaxis_title="Price")

    time_buttons = [
        {'step': 'all', 'label': 'All'},
        {'count': 3, 'step': 'year', 'stepmode': 'backward', 'label': '3 Year'},
        {'count': 1, 'step': 'year', 'stepmode': 'backward', 'label': '1 Year'},
        {'count': 6, 'step': 'month', 'stepmode': 'backward', 'label': '6 Month'},
        {'count': 1, 'step': 'month', 'stepmode': 'backward', 'label': '1 Month'},
        {'count': 1, 'step': 'year', 'stepmode': 'todate', 'label': '1 Year To Date'}
    ]

    fig_candlestick.update_layout(hovermode="x unified")
    fig_candlestick.update_xaxes(rangeselector={'buttons': time_buttons})
    fig_candlestick.update_yaxes(autorange=True, fixedrange = False)

    return fig_candlestick

def plot_kpis(stock_fig, ticker_symbol, length, kpi_name):

    indicator = get_technical_indicator(ticker_symbol, int(length), kpi_name)

    if kpi_name == 'MA':
        stock_fig.add_trace(go.Scatter(x=indicator['Date'], y=indicator[indicator.columns[1]], mode='lines', name=indicator.columns[1]))
        return stock_fig
    else:
        stock_data = get_stock_data(ticker_symbol)
        #fig = go.Figure()
        fig = make_subplots(rows=2, cols=1)

        fig.add_trace(go.Scatter(x=indicator['Date'], y=stock_data['Close'], mode='lines', name='Stock Close Price'), row=1, col=1)
        fig.update_xaxes(showticklabels=False, row=1, col=1)
        fig.add_trace(go.Scatter(x=indicator['Date'], y=indicator[indicator.columns[1]], mode='lines', name=kpi_name), row=2, col=1)

        fig.update_layout(hovermode='x unified')
        fig.update_traces(hoverinfo='x+y')

        return fig



# Plot interactive stock data
def plot_stock_data(ticker_symbol): # indicator
    stock_data = get_stock_data(ticker_symbol)

    fig = go.Figure()

    # Add trace for stock closing prices
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], mode='lines', name='Close'))
    # fig.add_trace(go.Scatter(x=indicator['Date'], y=indicator[indicator.columns[1]], mode='lines', name=indicator.columns[1]))

    time_buttons = [
        {'step': 'all', 'label': 'All'},
        {'count': 3, 'step': 'year', 'stepmode': 'backward', 'label': '3 Year'},
        {'count': 1, 'step': 'year', 'stepmode': 'backward', 'label': '1 Year'},
        {'count': 6, 'step': 'month', 'stepmode': 'backward', 'label': '6 Month'},
        {'count': 1, 'step': 'month', 'stepmode': 'backward', 'label': '1 Month'},
        {'count': 1, 'step': 'year', 'stepmode': 'todate', 'label': '1 Year To Date'}
    ]

    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(rangeselector={'buttons': time_buttons})
    fig.update_yaxes(autorange=True, fixedrange = False)
    fig.update_layout(xaxis_rangeslider_visible=True)

    # Update layout
    fig.update_layout(title='Interactive Stock Data Plot',
                      xaxis_title='Date', yaxis_title='Value')

    # Add tooltip
    fig.update_traces(hovertemplate="Date: %{x}<br>Close Price: %{y}")

    return fig

# Callback to update y-axis range when x-axis range is changed
def update_y_axis_range(fig, trace, points):
    x_data = points.xs[0]
    y_data = trace.y[int(x_data)]
    new_min = min(y_data)
    new_max = max(y_data)
    fig.update_yaxes(range=[new_min, new_max])
