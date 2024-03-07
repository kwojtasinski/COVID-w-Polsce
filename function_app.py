import azure.functions as func
from .covid_w_polsce.utils import (
    extract_latest_data,
    extract_poland_data,
    transform_poland_data,
)

app = func.FunctionApp()

@app.function_name(name="HttpTrigger1")
@app.route(route="get-df")
def main(req: func.HttpRequest) -> str:
    if req.params.get("year") == "latest":
        df = extract_latest_data()
    else:
        year = req.params.get("year")
        df = extract_poland_data(year)
        df = transform_poland_data(df)

    return df.to_json()