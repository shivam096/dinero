import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st

# Fetch stock data
def get_stock_data(symbol):  # start_date, end_date
    file_path = f'../data/{symbol}.csv'
    stock_data = pd.read_csv(file_path)
    return stock_data


# Plot interactive stock data
def plot_stock_data(stock_data):
    fig = go.Figure()

    # Add trace for stock closing prices
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Open'], mode='lines', name='Open'))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['High'], mode='lines', name='High'))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Low'], mode='lines', name='Low'))
    fig.add_trace(go.Scatter(x=stock_data['Date'], y=stock_data['Adj Close'], mode='lines', name='Adj Close'))
    # Add trace for stock volume
    # fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Volume'], mode='lines', name='Volume'))

    time_buttons = [
        {'step': 'all', 'label': 'All'},
        {'count': 1, 'step': 'month', 'stepmode': 'backward', 'label': '1 Month'},
        {'count': 6, 'step': 'month', 'stepmode': 'backward', 'label': '6 Month'},
        {'count': 1, 'step': 'year', 'stepmode': 'todate', 'label': '1 Year To Date'},
        {'count': 1, 'step': 'year', 'stepmode': 'backward', 'label': '1 Year'},
        {'count': 3, 'step': 'year', 'stepmode': 'backward', 'label': '3 Year'}
    ]

    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(rangeselector={'buttons': time_buttons})

    # Update layout
    fig.update_layout(title='Interactive Stock Data Plot', xaxis_title='Date', yaxis_title='Value')

    # Add tooltip
    fig.update_traces(hovertemplate="Date: %{x}<br>Close Price: %{y}")

    # fig['layout']['yaxis'].update(autorange = True)
    fig.update_layout
    layout = dict(
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

    def zoom(layout, xrange):
        in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
        fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

    fig.layout.on_change(zoom, 'xaxis.range')

    return fig

stock_data = get_stock_data('AAPL')
fig = plot_stock_data(stock_data)
st.plotly_chart(fig)



