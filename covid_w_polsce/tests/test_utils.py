from utils import transform_poland_data, extract_poland_data
import pandas as pd


def test_transform_poland_data():
    _2022 = transform_poland_data(extract_poland_data("2022"), "2022")
    _2021 = transform_poland_data(extract_poland_data("2021"), "2021")
    _2020 = transform_poland_data(extract_poland_data("2020"), "2020")

    assert isinstance(_2022, pd.DataFrame)
    assert isinstance(_2021, pd.DataFrame)
    assert isinstance(_2020, pd.DataFrame)

    assert _2022.compare(pd.read_csv("covid-w-polsce/2022.csv"))
    assert _2021.compare(pd.read_csv("covid-w-polsce/2021.csv"))
    assert _2020.compare(pd.read_csv("covid-w-polsce/2020.csv"))
