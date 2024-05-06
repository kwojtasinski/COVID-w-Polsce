from fastapi import Depends, FastAPI

from covid_backend.analytics import extract_poland_data, transform_poland_data
from covid_backend.storage import BaseStorageClient, get_storage_client

app = FastAPI()


@app.get("/get-df")
def get_df(year: int, client: BaseStorageClient = Depends(get_storage_client)) -> str:
    data = client.get_object("covid", str(year))
    if data is None:
        df = extract_poland_data(str(year))
        df = transform_poland_data(df, str(year))
        result = df.to_json()
        client.upload_object("covid", str(year), result)
        return result
    else:
        return data
