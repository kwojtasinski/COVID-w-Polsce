import azure.functions as func
from covid_w_polsce.utils import (
    extract_latest_data,
    extract_poland_data,
    transform_poland_data,
)
from azure.storage.blob import BlobServiceClient
import os
   
app = func.FunctionApp()

@app.route(route="get-df")
def main(req: func.HttpRequest) -> str:

    year = req.params.get("year")

    if year == "latest":
        df = extract_latest_data()
    else:
        df = extract_poland_data(year)
        df = transform_poland_data(df)

    blob_service_client = BlobServiceClient.from_connection_string(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))

    df.to_json("blob.json")
    blob_client = blob_service_client.get_blob_client(container=os.environ.get("STORAGE_CONTAINER"), blob=f"{year}.json")
    with open(file="blob.json", mode="rb") as data:
        blob_client.upload_blob(data)
        return data