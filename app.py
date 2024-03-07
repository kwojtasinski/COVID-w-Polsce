import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from azure.storage.blob import BlobServiceClient

os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'
os.environ['STORAGE_CONTAINER'] = 'test-container'

from covid_w_polsce.utils import (
    extract_latest_data,
    extract_poland_data,
    transform_poland_data,
)


def display_data(option: str):
    if option == "Latest worldwide":
        year = "latest"
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
    

    blob_service_client = BlobServiceClient.from_connection_string(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))

    df.to_json("blob.json")
    blob_client = blob_service_client.get_blob_client(container=os.environ.get("STORAGE_CONTAINER"), blob=f"{year}.json")
    with open(file="blob.json", mode="rb") as data:
        blob_client.upload_blob(data)


option = st.selectbox(
    "Wybierz rok",
    pd.Series(["Latest worldwide", "Poland 2020", "Poland 2021", "Poland 2022"]),
)

display_data(option)
