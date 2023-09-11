import pandas as pd
from streamlit_elements import elements, mui, dashboard, html, nivo

# from Typing import List

import streamlit as st

st.set_page_config(layout="wide")

st.title("CryptoCheck")

# Read data into a dataframe
df = pd.read_csv("./data/data.csv")


def reformat_df(data_frame):
    new_df = []
    for column in data_frame.columns[1:]:
        data_points = []

        for index, row in data_frame.iterrows():
            data_points.append({"x": row["date"], "y": int(row[column])})

        new_df.append({"id": column, "data": data_points})

    return new_df


# Create a list of coins to display
coins = []


# Create a function to filter the checkboxes based on the search query
def filter_checkboxes(search_query, cols):
    filtered_coins = []
    for col in cols:
        if search_query in col:
            filtered_coins.append(col)
    return filtered_coins


# TODO - Keep search results thorughout session
# TODO - Add a button to clear all checkboxes
# TODO - Search as each letter is typed
# TODO - Add a button to select all checkboxes
# TODO - Zoom on each graph appropriately (currently always contains 0)

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
            unsafe_allow_html=True,
        )
        with st.expander(
            label="Select coins to display (Graph will populate upon selection)"
        ):
            search_query = (
                st.text_input(
                    label="Search coins:",
                    placeholder="Search Ticker",
                    label_visibility="collapsed",
                )
                .strip()
                .upper()
            )

            # Define filtered coins outside of the loop
            filtered_coins = filter_checkboxes(search_query, df.columns[1:])

            cols_per_row = 10
            cols = st.columns(cols_per_row)

            # Populate the checkboxes with the filtered coins list
            for i, col in enumerate(filtered_coins, start=1):
                checkbox_col = cols[i % cols_per_row]
                checkbox_state = checkbox_col.checkbox(
                    col, key=None, label_visibility="visible"
                )

                if checkbox_state:
                    coins.append(col)

    # Dictionary to translate radio options to numerical values
    time_translate = {
        "Last 6 hours": 6,
        "Last 24 hours": 24,
        "Last 7 days": 168,
        "Last 30 days": 720,
        "Last 90 days": 2160,
        "Last 180 days": 4320,
        "Last 365 days": 8760,
    }

    # Only select columns that are checked
    if coins:
        with elements("dashboard"):
            layout = [
                # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
                dashboard.Item("graph", 0, 0, 15, 3),
                dashboard.Item(
                    "metrics",
                    2,
                    0,
                    2,
                    2,
                ),
            ]
            with dashboard.Grid(layout):
                with mui.Paper(
                    key="graph",
                    sx={
                        "display": "flex",
                        "flexDirection": "column",
                        "borderRadius": 3,
                        "overflow": "hidden",
                        "bgcolor": "white",
                    },
                    elevation=1,
                ):
                    # Time period selector
                    time_period = st.radio(
                        label="Select time period:",
                        options=["Last 6 hours", "Last 24 hours", "Last 7 days"],
                    )
                    selected_df = df[["date"] + coins].tail(time_translate[time_period])

                    formatted_df = reformat_df(selected_df)

                    # get maximum value from selected_df
                    max_value = selected_df[coins].max().max()
                    # get minimum value from selected_df
                    min_value = selected_df[coins].min().min()
                    # get range
                    range_value = max_value - min_value
                    st.write(selected_df)

                    # TODO FIX ROUNDING ISSUE

                    # Graph
                    with mui.Box(sx={"flex": 1, "minHeight": 0}):
                        nivo.Line(
                            data=formatted_df,
                            margin={"top": 50, "right": 110, "bottom": 50, "left": 60},
                            xScale={"type": "point"},
                            yScale={
                                "type": "linear",
                                "min": min_value - (range_value * 0.1),
                                "max": max_value + (range_value * 0.1),
                                "stacked": False,
                                "reverse": False,
                            },
                            yFormat=">-.8",
                            axisTop={"null"},
                            axisRight={"null"},
                            axisBottom={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "transportation",
                                "legendOffset": 36,
                                "legendPosition": "middle",
                            },
                            axisLeft={
                                "tickSize": 5,
                                "tickPadding": 5,
                                "tickRotation": 0,
                                "legend": "count",
                                "legendOffset": -40,
                                "legendPosition": "middle",
                            },
                            pointSize={10},
                            pointColor={"from": "color"},
                            pointLabelYOffset={-12},
                            enableSlices="x",
                            useMesh=True,
                            legends=[
                                {
                                    "anchor": "bottom-right",
                                    "direction": "column",
                                    "justify": False,
                                    "translateX": 120,
                                    "translateY": 0,
                                    "itemsSpacing": 0,
                                    "itemDirection": "left-to-right",
                                    "itemWidth": 80,
                                    "itemHeight": 20,
                                    "itemOpacity": 0.75,
                                    "symbolSize": 12,
                                    "symbolShape": "circle",
                                    "symbolBorderColor": "rgba(0, 0, 0, .5)",
                                    "effects": [
                                        {
                                            "on": "hover",
                                            "style": {
                                                "itemBackground": "rgba(0, 0, 0, .03)",
                                                "itemOpacity": 1,
                                            },
                                        }
                                    ],
                                }
                            ],
                            theme={
                                "background": "#ffffff",
                                "text": {
                                    "fontSize": 11,
                                    "fill": "#000",
                                    "outlineWidth": 0,
                                    "outlineColor": "transparent",
                                },
                                "tooltip": {
                                    "container": {
                                        "background": "#0F1116",
                                        "fontSize": 12,
                                    },
                                    "text": {
                                        "fill": "#000",
                                    },
                                    "basic": {},
                                    "chip": {},
                                    "table": {},
                                    "tableCell": {},
                                    "tableCellValue": {},
                                },
                            },
                        )

                    # with mui.Paper():
                    #     st.header(f"Price Chart for {', '.join(coins)}")
                    #     st.text(time_period)
                    #     st.line_chart(data=selected_df, x="date", y=coins, width=0, height=0, use_container_width=True)
                # with mui.Card(key="metrics"):
                #     mui.CardHeader(title="Metrics", className="draggable")
                #     with mui.CardContent(sx={"flex": 1}):
                #         mui.Paper("Change in last 1 hour")
                # for coin in coins:
                #     st.metric(label=coin, value=round(selected_df[coin].iloc[-1], 5), delta=round(selected_df[coin].iloc[-1] - selected_df[coin].iloc[-2], 10))
