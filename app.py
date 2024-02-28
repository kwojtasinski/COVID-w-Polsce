import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from covid_w_polsce.utils import (
    extract_latest_data,
    extract_poland_data,
    transform_poland_data,
)


def display_data(option: str):
    if option == "Latest worldwide":
        df = extract_latest_data()
        st.write(df)
    else:
        year = option[7:]
        df = extract_poland_data(year)
        df = transform_poland_data(df, year)
        st.write(df)

        df.to_json(f"{year}.json")
        st.line_chart(df[:-1], y="Total", use_container_width=True)
        st.pyplot(plt)


option = st.selectbox(
    "Wybierz rok",
    pd.Series(["Latest worldwide", "Poland 2020", "Poland 2021", "Poland 2022"]),
)

display_data(option)
