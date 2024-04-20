import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests

def display_data(option: str):

    if option == "Latest worldwide":
        response = requests.get(f"http://backend:8000/get-df?year=0")
        df = pd.read_json(response.json())
        st.write(df)
    else:
        year = option[7:]
        response = requests.get(f"http://backend:8000/get-df?year={year}")
        df = pd.read_json(response.json())
        df.sort_index(axis = 0, inplace=True)
                
        s = df.iloc[-1, 1:-1]
        s.name = ""
        s.plot.pie(autopct="%.1f%%")

        st.write(df)
        st.line_chart(df[:-1], y="Total", use_container_width=True)
        st.pyplot(plt)

    

    

 
    


option = st.selectbox(
    "Wybierz rok",
    pd.Series(["Latest worldwide", "Poland 2020", "Poland 2021", "Poland 2022"]),
)

display_data(option)
