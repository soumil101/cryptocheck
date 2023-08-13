import requests
import json
import datetime
import pandas as pd
# from Typing import List

import streamlit as st

st.title("CryptoCheck")

# Read data into a dataframe
df = pd.read_csv("./data/_test.csv")

coins = []

expander = st.expander(label='Select coins to display')

# Create a scrollable container
with st.container():
    with expander:
        for col in df.columns[1:]:
            globals()[col] = st.checkbox(col, value=True, key=None, label_visibility="visible")
            if globals()[col]:
                coins.append(col)

    # Apply custom CSS to make the container scrollable
    st.markdown(
        """
        <style>
        .st-cn {
            display: flex;
            flex-wrap: wrap;
            max-height: 400px;  /* Adjust the max height as needed */
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

st.title("ETH Price Chart")
st.line_chart(data=df, x="date", y=coins, width=0, height=1000, use_container_width=True)
