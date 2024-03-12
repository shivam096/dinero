import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

from backend.visualization import plot_stock_price
from backend.visualization import plot_kpis
from backend.kpi_manager import get_technical_indicator
from backend.stock_data_manager import download_stock_data, update_stock_data, get_existing_tickers, get_last_n_days
from backend.processing import get_sentiments


st.set_page_config(layout="wide")

heading_color = "#86B6F6"
news_article_color = "#E3DFFD"
news_article_date_color = "#89CFF3"
title_color = "#DBE7C9"
positive_color = "#527853"  # Green
neutral_color = "#B4B4B8"    # Yellow
negative_color = "#D24545"   # Red

# df = pd.DataFrame(data)
# df['Date'] = pd.to_datetime(df['Date'])

st.title("Cool chart!")
kpi_description_mapping = {
    "MA" : "The <span style='color:#D24545'><b>Moving Average (MA)</b></span> helps <span style='color:#AEDEFC'><i>smooth out short-term price fluctuations</i></span> to reveal the underlying trend. Imagine calculating the average price of a stock over a set period (like 20 days or 50 days). This helps <span style='color:#AEDEFC'><i>visualize the general direction (upward, downward, or sideways)</i></span> and spot trends to figure out when the stock might change direction.",
    "RSI": "<span style='color:#D24545'><b>Relative Strength Index (RSI)</b></span> is like a speedometer for stocks! It tells us <span style='color:#AEDEFC'><i>how fast the price of a stock is changing.</i></span> When RSI is <span style='color:#AEDEFC'><i>high</i></span>, it means the stock might be <span style='color:#AEDEFC'><i>going up too fast and could slow down.</i></span> When RSI is <span style='color:#AEDEFC'><i>low</i></span>, it means the stock might be <span style='color:#AEDEFC'><i>going down too fast and could bounce back up.</i></span>",
    "ROC": "<span style='color:#D24545'><b>Rate of Change (ROC)</b></span> tells you <span style='color:#AEDEFC'><i>how much the price has changed over a certain period of time,</i></span> expressed as a percentage. <span style='color:#AEDEFC'><i>Positive ROC</i></span> means the <span style='color:#AEDEFC'><i>price is going up,</i></span> <span style='color:#AEDEFC'><i>negative ROC</i></span> means it's <span style='color:#AEDEFC'><i>going down.</i></span> It helps you understand <span style='color:#AEDEFC'><i>how quickly the price is moving in one direction or another.</i></span>",
    "BBP": "<span style='color:#D24545'><b>Bollinger Bands Percentage (BBP)</b></span> is like a rubber band around a stock's price! These bands are a <span style='color:#AEDEFC'><i>volatility indicator</i></span>, with a <span style='color:#AEDEFC'><i>wider band signifying higher volatility</i></span> and a <span style='color:#AEDEFC'><i>narrower band indicating lower volatility.</i></span> BBP values close to 0 suggest the price is near the lower band, potentially <span style='color:#AEDEFC'><i>hinting at oversold conditions</i></span>. Conversely, values close to 100 indicate the price is near the upper band, potentially <span style='color:#AEDEFC'><i>suggesting overbought conditions.</i></span>"
}

kpi_chart_info_mapping = {
"MA": "When a stock price increeases above the <span style='color:#D24545'><b>moving average</b></span> line it can signal an <span style='color:#AEDEFC'><i>upward trend</i></span> and a <span style='color:#AEDEFC'><i>potential buying opportunity.</i></span> Conversely, if the <span style='color:#AEDEFC'><i>stock price falls below a moving average,</i></span> it might <span style='color:#AEDEFC'><i>indicate a downtrend</i></span> and a <span style='color:#AEDEFC'><i>potential selling point.</i></span> The slope of the moving average can also provide insight into the <span style='color:#AEDEFC'><i>market's direction.</i></span>",
"RSI": "An <span style='color:#D24545'><b>RSI </b></span> value <span style='color:#AEDEFC'><i>above 70</i></span> indicates that a <span style='color:#AEDEFC'><i>stock may be overbought,</i></span> suggesting a <span style='color:#AEDEFC'><i>potential sell signal,</i></span> while a value <span style='color:#AEDEFC'><i>below 30</i></span> might indicate that a <span style='color:#AEDEFC'><i>stock is oversold,</i></span> pointing to a <span style='color:#AEDEFC'><i>potential buy signal.</i></span> Values <span style='color:#AEDEFC'><i>in between can suggest a market in <span style='color:#AEDEFC'><i>equilibrium,</i></span> with <span style='color:#AEDEFC'><i>no clear overbought or oversold signals.</i></span>",
"ROC": "A <span style='color:#D24545'><b>ROC </b></span>value <span style='color:#AEDEFC'><i>above zero</i></span> suggests an <span style='color:#AEDEFC'><i>upward momentum,</i></span> potentially indicating a <span style='color:#AEDEFC'><i>buying opportunity,</i></span> while a value <span style='color:#AEDEFC'><i>below zero can indicate <span style='color:#AEDEFC'><i>downward momentum,</i></span> suggesting a <span style='color:#AEDEFC'><i>selling or short-selling opportunity.</i></span> The farther the ROC moves from zero, the stronger the indicated momentum.",
"BBP" : "A <span style='color:#D24545'><b>BBP</b></span> value <span style='color:#AEDEFC'><i>above 1</i></span> indicates a <span style='color:#AEDEFC'><i>price exceeding the upper Bollinger Band,</i></span> which could signal an <span style='color:#AEDEFC'><i>overbought condition,</i></span> while a value <span style='color:#AEDEFC'><i>below 0</i></span> indicates a <span style='color:#AEDEFC'><i>price below the lower band,</i></span> potentially signaling an <span style='color:#AEDEFC'><i>oversold condition.</i></span> Values <span style='color:#AEDEFC'><i>close to 0.5</i></span> suggest the price is near the middle band, indicating a <span style='color:#AEDEFC'><i>lack of strong trend.</i></span>"
}

st.image("frontend/logo.png", use_column_width=True)

# # percentage_change_option = st.sidebar.selectbox('Select Percentage Change in Stock Price', ('10%', '5%', '-5%', '-10%'))
# percentage_change_option = st.sidebar.selectbox('Select Percentage Change in Stock Price', (10, 5, -5, -10))

tab1, tab2, tab3, tab4 = st.tabs(["📈 Stock Performance Overview", "🔍 Explore Stock Technical Indicators", "📰 Latest News Headlines and Articles", "💡 Explore More Tickers or Update Data!"])

with tab1:
    #st.markdown(f"<h4 style='color:{title_color};'></h4>", unsafe_allow_html=True)
    company_option = st.selectbox('Choose the Company Stock you Wish to View!', set(get_existing_tickers()))
    st.markdown(f"<h2 style='color:{heading_color}; text-align: center;'>{company_option} : STOCK PERFORMANCE VISUALIZATION</h2>", unsafe_allow_html=True)
    # create vis
    fig_price = plot_stock_price(company_option)

    # Store the initial view as session state
    if 'initial_view' not in st.session_state:
        st.session_state.initial_view = fig_price.to_dict()

    st.plotly_chart(fig_price, use_container_width=True)

    # "Return to Initial View" button
    if st.button('Return to Initial View'):
        fig_price.update(st.session_state.initial_view)

    with st.expander(f"🛈 How to Read a Candlestick Chart?"):
        st.markdown("Blah Blah", unsafe_allow_html=True)

with tab2:
    st.markdown("<h2 style='color:{}; text-align: center;'>LEVERAGING TECHNICAL INDICATORS</h2>".format(heading_color), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        kpi_name = st.selectbox('Select Technical Indicator', ('MA', 'RSI', 'ROC', 'BBP'))
        with st.expander(f"🛈 More about {kpi_name}"):
            st.markdown(kpi_description_mapping[kpi_name], unsafe_allow_html=True)

    with col2:
        length = st.number_input('Input a length', value=100, format='%d')

        with st.expander(f"🛈 What is length?"):
                st.markdown("<span style='color:#D24545'><b>Length</b></span> typically refers to the <span style='color:#AEDEFC'><b>number of days</b></span> over which the KPI is calculated.".format(positive_color), unsafe_allow_html=True)


    fig_kpi = plot_kpis(fig_price, company_option, length, kpi_name)
    #st.plotly_chart(fig_kpi, use_container_width=True)

    if fig_kpi:
        st.plotly_chart(fig_kpi, use_container_width=True)
    else:
        st.plotly_chart(fig_price, use_container_width=True)

    with st.expander(f"🛈 What do These Numbers Mean?"):
        st.markdown(kpi_chart_info_mapping[kpi_name], unsafe_allow_html=True)

with tab3:
    st.markdown("<h2 style='color:{}; text-align: center;'>BEYOND HEADLINES : DECODING NEWS SENTIMENT</h2>".format(heading_color), unsafe_allow_html=True)
    # Display the metrics in a single row
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        number_of_days = st.number_input('Select News Date Range 📅 (eg. 30 days, 60 days)', value=90, format='%d')

    with input_col2:
        percentage_change_option = st.number_input('Choose Stock Price Change % 📈', value=5, format='%d')

    df = get_sentiments(company_option, percentage_change_option)
    df = get_last_n_days(df,number_of_days)
    df['Date'] = pd.to_datetime(df['Date'])
    # df.reset_index(inplace=True)

    col1, col2, col3 = st.columns(3)
    if df.empty:
        st.write("<h5 style='color:{}; text-align: center;'>Oops! 😔 We couldn't find any headlines matching your selected filters.</h5>".format(title_color), unsafe_allow_html=True)
        st.write("<h5 style='color:{}; text-align: center;'>📰 Try adjusting the date range or changing the percentage change in prices to discover more news stories! 💡</h5>".format(title_color),unsafe_allow_html=True)
    else:
        with col1:
            average_positive_score = round(df['Positive Sentiment Score'].mean(),2)
            average_negative_score = round(df['Negative Sentiment Score'].mean(),2)
            average_neutral_score = round(df['Neutral Sentiment Score'].mean(),2)

            st.markdown(f"<h1 style='color:{positive_color}; text-align: center;'>{average_positive_score}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Positive Sentiment Score 😄</p>", unsafe_allow_html=True)

        # Metric 2: Neutral Sentiment Score
        with col2:
            st.markdown(f"<h1 style='color:{neutral_color}; text-align: center;'>{average_neutral_score}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Neutral Sentiment Score 😐</p>", unsafe_allow_html=True)

        # Metric 3: Negative Sentiment Score
        with col3:
            st.markdown(f"<h1 style='color:{negative_color}; text-align: center;'>{average_negative_score}</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Negative Sentiment Score ☹️</p>", unsafe_allow_html=True)

        st.markdown('<hr class="horizontal-line">', unsafe_allow_html=True)

        for index, row in df.iterrows():

            with st.container():
                st.markdown(f"<h4><span style='color:{news_article_date_color}'>{row['Date'].strftime('%B %d, %Y')} : </span><span><a href='{row['Link']}' target='_blank' style='color:{news_article_color}'>{row['Title']}</a></span></h4>", unsafe_allow_html=True)
            # with st.expander(f"{row['Date'].strftime('%Y-%m-%d')}: {row['Title']}"):
                df_col1, df_col2, df_col3 = st.columns(3)
                with df_col1:
                    st.markdown(f"<h6 style='color:{positive_color}'>Positive Sentiment Score: <code style='color:{positive_color}'>{row['Positive Sentiment Score']}</code></h6>", unsafe_allow_html=True)
                with df_col2:
                    st.markdown(f"<h6 style='color:{neutral_color}'>Neutral Sentiment Score: <code style='color:{neutral_color}'>{row['Neutral Sentiment Score']}</code></h6>", unsafe_allow_html=True)
                with df_col3:
                    st.markdown(f"<h6 style='color:{negative_color}'>Negative Sentiment Score:<code style='color:{negative_color}'>{row['Negative Sentiment Score']}</code></h6>", unsafe_allow_html=True)

                st.markdown('<hr class="horizontal-line">', unsafe_allow_html=True)

with tab4:
    selected_ticker = st.text_input('➕ Add New Ticker')
    selected_time = st.text_input("🕒 Input a time period [valid formats include days ('d'), weeks ('wk'), months ('mo'), years ('y')]")

    if st.button("🔄 Update Ticker Data"):

        selected_ticker = selected_ticker.upper()

        if len(selected_time) == 0:
            download_stock_data(selected_ticker)
        else:
            selected_time = selected_time.lower()
            if not (selected_time == 'max' or selected_time[-1] in ['d','y'] or selected_time[-2:] in ['wk','mo']):
                raise ValueError("period_str formats: 'max', 'd', 'wk', 'mo', 'y' (case insensitive).")
            download_stock_data(selected_ticker, selected_time)
            st.experimental_rerun()
    if st.button("🔁 Click to Update Ticker Data to the Most Recent"):
        update_stock_data()
        st.experimental_rerun()