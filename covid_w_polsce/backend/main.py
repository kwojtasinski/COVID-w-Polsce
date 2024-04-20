from backend.utils import (
    extract_latest_data,
    extract_poland_data,
    transform_poland_data,
)
from azure.storage.blob import BlobServiceClient
from fastapi import FastAPI
import os
from io import StringIO


#default 

if os.environ.get('AZURE_STORAGE_CONNECTION_STRING') is None:
    os.environ['AZURE_STORAGE_CONNECTION_STRING'] = 'DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;'

if os.environ.get('STORAGE_CONTAINER') is None:   
    os.environ['STORAGE_CONTAINER'] = 'test-container'
   
app = FastAPI()

@app.get("/get-df")
def main(year : int) -> str:

    if year == 0:
        df = extract_latest_data()
    elif year == 2020 or year == 2021 or year == 2022:
        df = extract_poland_data(str(year))
        df = transform_poland_data(df, str(year))
    else:
        return "invalid parameters"

    blob_service_client = BlobServiceClient.from_connection_string(os.environ.get("AZURE_STORAGE_CONNECTION_STRING"))

    lst = [i for i in blob_service_client.list_containers(name_starts_with=os.environ.get("STORAGE_CONTAINER"))] 
    if not lst:
        blob_service_client.create_container(os.environ.get("STORAGE_CONTAINER"))

    buff = StringIO()
    df.to_json(buff)
    data = buff.getvalue()
    blob_client = blob_service_client.get_blob_client(container=os.environ.get("STORAGE_CONTAINER"), blob=f"{year}.json")


    blob_client.upload_blob(bytes(data, "UTF-8"), overwrite=True)

    return data
    


    