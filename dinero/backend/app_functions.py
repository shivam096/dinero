import pandas as pd
import streamlit as st

def retrieve_data(company_option):
    file_path = f'dinero/data/{company_option}.csv'
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df.reset_index(inplace=True)
    return df

def streamlit_filtering_by_date(df):

    default_start_date = df['Date'].iloc[0]
    default_end_date = df['Date'].iloc[-1]

    start_date = st.sidebar.date_input('Start date', default_start_date )
    end_date = st.sidebar.date_input('End date', default_end_date )
    # Convert Python date objects to Pandas datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if start_date < end_date:
        st.sidebar.success(f'Start date: `{start_date}`\n\nEnd date:`{end_date}`')
    else:
        st.sidebar.error('Error: End date must fall after start date.')

    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df.reset_index(inplace=True)
    return df




