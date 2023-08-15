import requests
import json
import datetime
import pandas as pd
# from Typing import List

import streamlit as st

st. set_page_config(layout="wide")

st.title("CryptoCheck")

# Read data into a dataframe
df = pd.read_csv("./data/data.csv")

# Create a list of coins to display
coins = []

# Create a function to filter the checkboxes based on the search query
def filter_checkboxes(search_query, cols):
    filtered_coins = []
    search_query = search_query.upper()
    for col in cols:
        if search_query in col:
            filtered_coins.append(col)
    return filtered_coins

#TODO - Keep search results thorughout session
#TODO - Add a button to clear all checkboxes
#TODO - Search as each letter is typed
#TODO - Add a button to select all checkboxes
#TODO - Zoom on each graph appropriately (currently always contains 0)

# Create a scrollable container
with st.container():
    with st.container():
        # Apply custom CSS to make the container scrollable
        st.markdown(
            """
            <style>
            .st-cn {
                max-height: 200px; 
                overflow-y: auto;
                border: 1px solid #ccc;
                padding: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with st.expander(label='Select coins to display (Graph will populate upon selection)'):
    
    # Apply custom CSS to make the container scrollable
            search_query = st.text_input(label="Search coins:", placeholder="Search Ticker", label_visibility="collapsed").strip().upper()

            # Define filtered coins outside of the loop
            filtered_coins = filter_checkboxes(search_query, df.columns[1:])

            cols_per_row = 10
            cols = st.columns(cols_per_row)

            # Populate the checkboxes with the filtered coins list
            for i, col in enumerate(filtered_coins, start=1):
                checkbox_col = cols[i % cols_per_row]
                checkbox_state = checkbox_col.checkbox(col, key=None, label_visibility="visible")

                if checkbox_state:
                    coins.append(col)

    # Dictionary to translate radio options to numerical values
    time_translate = {"Last 6 hours": 6, "Last 24 hours": 24, "Last 7 days": 168, "Last 30 days": 720, "Last 90 days": 2160, "Last 180 days": 4320, "Last 365 days": 8760}
    
    # Only select columns that are checked
    if coins:
        # Time period selector
        time_period = st.radio(label="Select time period:", options=["Last 6 hours", "Last 24 hours", "Last 7 days"])
        selected_df = df[["date"] + coins].tail(time_translate[time_period])

        with st.container():
            st.header(f"Price Chart for {', '.join(coins)}")
            st.text(time_period)
            st.line_chart(data=selected_df, x="date", y=coins, width=0, height=0, use_container_width=True)
        
        # Create a container to display the metrics of each coin
        with st.container():
            st.text("Change in last 1 hour")
            for coin in coins:
                st.metric(label=coin, value=round(selected_df[coin].iloc[-1], 5), delta=round(selected_df[coin].iloc[-1] - selected_df[coin].iloc[-2], 10))

    st.markdown(
        """
        <style>
        .st-ch {
            display: flex;
            flex-direction: horizontal;
            width: 100%;
            }
            </style>
            """,
        unsafe_allow_html=True
    )
