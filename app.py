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
    for col in cols:
        if search_query in col:
            filtered_coins.append(col)
    return filtered_coins

#TODO - Keep search results thorughout session
#TODO - Add a button to clear all checkboxes
#TODO - Search as each letter is typed

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
            search_query = st.text_input(label="Search coins:", placeholder="Search Ticker", label_visibility="collapsed").strip()

            # Define filtered coins outside of the loop
            filtered_coins = filter_checkboxes(search_query, df.columns[1:])

            cols_per_row = 10
            cols = st.columns(cols_per_row)

            # Populate the checkboxes with the filtered coins list
            for i, col in enumerate(filtered_coins, start=1):
                checkbox_col = cols[i % cols_per_row]
                checkbox_state = checkbox_col.checkbox(col, value=False, key=None, label_visibility="visible")

                if checkbox_state:
                    coins.append(col)


    # Only select columns that are checked
    if coins:
        selected_df = df[["date"] + coins]
        with st.container():
            st.header(f"Price Chart for {', '.join(coins)}")
            st.line_chart(data=selected_df, x="date", y=coins, width=0, height=0, use_container_width=True)

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
