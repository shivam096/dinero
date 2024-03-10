import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from backend.visualization import plot_stock_price
from backend.visualization import plot_kpis
from backend.kpi_manager import get_technical_indicator
from backend.app_functions import retrieve_data, streamlit_filtering_by_date
from backend.stock_data_manager import download_stock_data, update_stock_data, get_existing_tickers


st.set_page_config(layout="wide")

heading_color = "#86B6F6"
title_color = "#DBE7C9"
positive_color = "#527853"  # Green
neutral_color = "#B4B4B8"    # Yellow
negative_color = "#D24545"   # Red

data = {
    'Date': ['2023-01-05', '2023-01-07', '2023-01-07', '2023-01-10', '2023-01-12',
             '2023-01-15', '2023-01-18', '2023-01-20', '2023-01-20', '2023-01-25'],
    'Headline': ['Breaking news: Stock market hits new high!',
                 'Tech company announces record profits',
                 'Market reacts to geopolitical events',
                 'Analysts bullish on energy sector',
                 'Economic outlook remains uncertain',
                 'Federal Reserve announces interest rate hike',
                 'Trade talks with China stall',
                 'Investors cautious amid global tensions',
                 'New product launch receives positive reviews',
                 'Company CEO resigns, stock price drops'],
    'Positive Sentiment Score': [0.8, 0.9, 0.7, 0.85, 0.75, 0.8, 0.65, 0.7, 0.9, 0.6],
    'Neutral Sentiment Score': [0.4, 0.5, 0.6, 0.4, 0.6, 0.3, 0.7, 0.5, 0.4, 0.6],
    'Negative Sentiment Score': [0.1, 0.2, 0.3, 0.15, 0.25, 0.2, 0.35, 0.4, 0.1, 0.5]
}

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])


# company_stock_mapping = {
#     "AAPL" : "APPLE",
#     "GOOG" : "GOOGLE",
#     "MSFT" : "MICROSOFT",
#     "NVDA" : "NVIDIA",
#     "TSLA" : "TESLA"
# }

kpi_description_mapping = {
    "MA" : "The <span style='color:#D24545'><b>Moving Average (MA)</b></span> helps <span style='color:#AEDEFC'><i>smooth out short-term price fluctuations</i></span> to reveal the underlying trend. Imagine calculating the average price of a stock over a set period (like 20 days or 50 days). This helps <span style='color:#AEDEFC'><i>visualize the general direction (upward, downward, or sideways)</i></span> and spot trends to figure out when the stock might change direction.",
    "RSI": "<span style='color:#D24545'><b>Relative Strength Index (RSI)</b></span> is like a speedometer for stocks! It tells us <span style='color:#AEDEFC'><i>how fast the price of a stock is changing.</i></span> When RSI is <span style='color:#AEDEFC'><i>high</i></span>, it means the stock might be <span style='color:#AEDEFC'><i>going up too fast and could slow down.</i></span> When RSI is <span style='color:#AEDEFC'><i>low</i></span>, it means the stock might be <span style='color:#AEDEFC'><i>going down too fast and could bounce back up.</i></span>",
    "ROC": "<span style='color:#D24545'><b>Rate of Change (ROC)</b></span> tells you <span style='color:#AEDEFC'><i>how much the price has changed over a certain period of time,</i></span> expressed as a percentage. <span style='color:#AEDEFC'><i>Positive ROC</i></span> means the <span style='color:#AEDEFC'><i>price is going up,</i></span> <span style='color:#AEDEFC'><i>negative ROC</i></span> means it's <span style='color:#AEDEFC'><i>going down.</i></span> It helps you understand <span style='color:#AEDEFC'><i>how quickly the price is moving in one direction or another.</i></span>",
    "BBP": "<span style='color:#D24545'><b>Bollinger Bands Percentage (BBP)</b></span> is like a rubber band around a stock's price! These bands are a <span style='color:#AEDEFC'><i>volatility indicator</i></span>, with a <span style='color:#AEDEFC'><i>wider band signifying higher volatility</i></span> and a <span style='color:#AEDEFC'><i>narrower band indicating lower volatility.</i></span> BBP values close to 0 suggest the price is near the lower band, potentially <span style='color:#AEDEFC'><i>hinting at oversold conditions</i></span>. Conversely, values close to 100 indicate the price is near the upper band, potentially <span style='color:#AEDEFC'><i>suggesting overbought conditions.</i></span>"
}

st.image("frontend/logo.png", use_column_width=True)

st.sidebar.header("Filters for Data")
company_option = st.sidebar.selectbox('Select one symbol', set(get_existing_tickers()))

percentage_change_option = st.sidebar.selectbox('Select Percentage Change in Stock Price', ('10%', '5%', '-5%', '-10%'))

tab1, tab2,tab3 = st.tabs(["Stock Visualizations and Technical Indicators", "News Headlines and Articles", "Download Data"])

with tab1:
    st.markdown("<h2 style='color:{}; text-align: center;'>{} STOCK PERFORMANCE VISUALIZATION</h2>".format(heading_color, company_option), unsafe_allow_html=True)
    # create vis
    fig_price = plot_stock_price(company_option)

    # Store the initial view as session state
    if 'initial_view' not in st.session_state:
        st.session_state.initial_view = fig_price.to_dict()

    st.plotly_chart(fig_price, use_container_width=True)

    # "Return to Initial View" button
    if st.button('Return to Initial View'):
        fig_price.update(st.session_state.initial_view)

    st.markdown("<h2 style='color:{}; text-align: center;'>LEVERAGING TECHNICAL INDICATORS</h2>".format(heading_color), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        kpi_name = st.selectbox('Select Technical Indicator', ('MA', 'RSI', 'ROC', 'BBP'))
        with st.expander(f"🛈 More about {kpi_name}"):
            st.markdown(kpi_description_mapping[kpi_name], unsafe_allow_html=True)

    with col2:
        length = st.number_input('Input a length')

        with st.expander(f"🛈 What is length?"):
                st.markdown("<span style='color:#D24545'><b>Length</b></span> typically refers to the <span style='color:#AEDEFC'><b>number of days</b></span> over which the KPI is calculated.".format(positive_color), unsafe_allow_html=True)


    fig_kpi = plot_kpis(fig_price, company_option, length, kpi_name)
    #st.plotly_chart(fig_kpi, use_container_width=True)

    if fig_kpi:
        st.plotly_chart(fig_kpi, use_container_width=True)
    else:
        st.plotly_chart(fig_price, use_container_width=True)


with tab2:
    st.markdown("<h2 style='color:{}; text-align: center;'>BEYOND HEADLINES : DECODING NEWS SENTIMENT</h2>".format(heading_color), unsafe_allow_html=True)
    # Display the metrics in a single row

    col1, col2, col3 = st.columns(3)
    with col1:
        average_positive_score = round(df['Positive Sentiment Score'].mean(),2)
        average_negative_score = round(df['Negative Sentiment Score'].mean(),2)
        average_neutral_score = round(df['Neutral Sentiment Score'].mean(),2)
        # average_compound_score = round(df['Compound Sentiment Score'].mean(),2)

        st.markdown("<h1 style='color:{positive_color}; text-align: center;'>{average_positive_score}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Positive Sentiment Score 😄</p>", unsafe_allow_html=True)

    # Metric 2: Neutral Sentiment Score
    with col2:
        st.markdown("<h1 style='color:{neutral_color}; text-align: center;'>{average_neutral_score}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Neutral Sentiment Score 😐</p>", unsafe_allow_html=True)

    # Metric 3: Negative Sentiment Score
    with col3:
        st.markdown("<h1 style='color:{negative_color}; text-align: center;'>{average_negative_score}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Negative Sentiment Score ☹️</p>", unsafe_allow_html=True)

    if df.empty:
        st.write("No headlines found")
    else:
        for index, row in df.iterrows():
            with st.expander(f"{row['Date'].strftime('%Y-%m-%d')}: {row['Title']}"):
                df_col1, df_col2, df_col3 = st.columns(3)
                with df_col1:
                    st.markdown(f"<span style='color:{positive_color}'>Positive Sentiment Score:</span> <code style='color:{positive_color}'>{row['Positive Sentiment Score']}</code>", unsafe_allow_html=True)
                with df_col2:
                    st.markdown(f"<span style='color:{neutral_color}'>Neutral Sentiment Score:</span> <code style='color:{neutral_color}'>{row['Neutral Sentiment Score']}</code>", unsafe_allow_html=True)
                with df_col3:
                    st.markdown(f"<span style='color:{negative_color}'>Negative Sentiment Score:</span> <code style='color:{negative_color}'>{row['Negative Sentiment Score']}</code>", unsafe_allow_html=True)

with tab3:
    selected_ticker = st.text_input('Input a ticker symbol:')
    selected_time = st.text_input('Input a time period')

    if st.button("Click button to download data"):

        selected_ticker = selected_ticker.upper()

        if len(selected_time) == 0:
            download_stock_data(selected_ticker)
        else:
            selected_time = selected_time.lower()
            if not (selected_time == 'max' or selected_time[-1] in ['d','y'] or selected_time[-2:] in ['wk','mo']):
                raise ValueError("period_str formats: 'max', 'd', 'wk', 'mo', 'y' (case insensitive).")
            download_stock_data(selected_ticker, selected_time)

    if st.button("Click button to update data"):
        update_stock_data()