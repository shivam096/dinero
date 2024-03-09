import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go

from dinero.backend.app_functions import retrieve_data, streamlit_filtering_by_date

heading_color = "#86B6F6"
title_color = "#DBE7C9"
st.set_page_config(layout="wide")

st.image("dinero/frontend/logo.png", use_column_width=True)

st.sidebar.header("Filters for Data")
company_option = st.sidebar.selectbox('Select one symbol', ('AAPL', 'GOOG', 'MSFT'))


df = retrieve_data(company_option)
df = streamlit_filtering_by_date(df)
progress_bar = st.progress(0)

percentage_change_option = st.sidebar.selectbox('Select Percentage Change in Stock Price', ('10%', '5%', '-5%', '-10%'))

tab1, tab2 = st.tabs(["Stock Visualizations and Technical Indicators", "News Headlines and Articles"])

company_stock_mapping = {
    "AAPL" : "APPLE",
    "GOOG" : "GOOGLE",
    "MSFT" : "MICROSOFT"
}

with tab1:
    st.markdown("<h2 style='color:{}; text-align: center;'>{} STOCK PERFORMANCE VISUALIZATION</h2>".format(heading_color, company_stock_mapping[company_option]), unsafe_allow_html=True)
    #st.header("Stock Visualizations and Technical Indicators")

    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))

    buttons = []
    for i in range(len(df)):
        date = df['Date'][i]
        close_price = df['Close'][i]
        button = dict(label=str(date), method='update', args=[{'x': [[date]], 'y': [[close_price]]}])
        buttons.append(button)

    fig_line.update_layout(updatemenus=[{'buttons': buttons,
                                    'direction': 'down',
                                    'showactive': True,
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'y': 1.15,
                                    'yanchor': 'top'}],
                    title="Stock Prices Over Time",
                    xaxis_title="Date", yaxis_title="Price")

    fig_line.update_traces(hovertemplate="Date: %{x}<br>Close Price: %{y}")

    # Show line chart
    st.plotly_chart(fig_line)

    st.markdown("<h2 style='color:{}; text-align: center;'>LEVERAGING TECHNICAL INDICATORS</h2>".format(heading_color), unsafe_allow_html=True)
    st.selectbox('Select Technical Indicator', ('MA', 'RSI', 'ROI', 'BBP'))
    tooltip_text = "This is where you input the length."

    length = st.number_input('Input a length')
    # Create a figure for candlestick chart - Demo/Trial
    fig_candlestick = go.Figure()

    # Add trace for candlestick chart
    fig_candlestick.add_trace(go.Candlestick(x=df['Date'],
                                            open=df['Open'],
                                            high=df['High'],
                                            low=df['Low'],
                                            close=df['Close'],
                                            name='Candlestick'))

    # Update layout for candlestick chart
    fig_candlestick.update_layout(title="Candlestick Chart",
                                xaxis_title="Date", yaxis_title="Price")

    # Show candlestick chart
    st.plotly_chart(fig_candlestick)


with tab2:
    st.markdown("<h2 style='color:{}; text-align: center;'>BEYOND HEADLINES : DECODING NEWS SENTIMENT</h2>".format(heading_color), unsafe_allow_html=True)
    with st.expander(f"**Headline**"):
        st.write("This is the News Article (if relevant)")

    # Define the colors for the "value" fields
    positive_color = "#527853"  # Green
    neutral_color = "#B4B4B8"    # Yellow
    negative_color = "#D24545"   # Red

    # Display the metrics in a single row

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h1 style='color:{}; text-align: center;'>0.70</h1>".format(positive_color), unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Positive Sentiment Score 😄</p>", unsafe_allow_html=True)

    # Metric 2: Neutral Sentiment Score
    with col2:
        st.markdown("<h1 style='color:{}; text-align: center;'>0.50</h1>".format(neutral_color), unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Neutral Sentiment Score 😐</p>", unsafe_allow_html=True)

    # Metric 3: Negative Sentiment Score
    with col3:
        st.markdown("<h1 style='color:{}; text-align: center;'>0.23</h1>".format(negative_color), unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Negative Sentiment Score ☹️</p>", unsafe_allow_html=True)


