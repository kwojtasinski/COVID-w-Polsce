import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

pd.options.mode.chained_assignment = None

plt.close("all")


def extract_latest_data() -> pd.DataFrame:
    return pd.read_csv(
        "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv"
    )


def extract_poland_data(year) -> pd.DataFrame:
    dfs = pd.read_html(
        "https://pl.wikipedia.org/wiki/Statystyki_pandemii_COVID-19_w_Polsce",
        match=f"Zakażenia w województwach w {year}",
        thousands=" ",
    )
    return dfs[0]


def transform_poland_data(df, year) -> pd.DataFrame:
    # usunięcie pustych/niepotrzebnych kolumn i wierszy
    df.columns = df.columns.droplevel([0, 1])
    df = df.iloc[:, :-7]
    df = df.drop(df.columns[[1, 2, 3]], axis=1)
    df = df.drop(df.tail(5).index)
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.index += 1

    if year == "2022":
        df.columns = df.columns.droplevel([1])
        df = df[df["pomorskie"].str.contains("2022") is False]

    # dwa rodzaje używanych myślników
    df.replace(to_replace="–", value=0, inplace=True)
    df.replace(to_replace="-", value=0, inplace=True)

    # zamiana typu danych
    for column in df.columns:
        if column == "Data":
            continue
        df[column] = df[column].astype(int)

    # dodanie kolumny i wiersza z sumowaniem
    df.loc[:, "Total"] = df.sum(numeric_only=True, axis=1)
    df.loc["Total"] = df.sum(numeric_only=True, axis=0)

    # znowu zmiana typu danych na int (zmieniaja sie na float?)
    for column in df.columns:
        if column == "Data":
            continue
        df[column] = df[column].astype(int)

    # generowanie wykresu procentowego udziału województw
    s = df.iloc[-1, 1:-1]
    s.name = ""
    s.plot.pie(autopct="%.1f%%")

    return df


def display_data(option):
    if option == "Latest worldwide":
        df = extract_latest_data()
        st.write(df)
    else:
        year = option[7:]
        df = extract_poland_data(year)
        df = transform_poland_data(df, year)
        st.write(df)
        st.line_chart(df[:-1], y="Total", use_container_width=True)
        st.pyplot(plt)


option = st.selectbox(
    "Wybierz rok",
    pd.Series(["Latest worldwide", "Poland 2020", "Poland 2021", "Poland 2022"]),
)

display_data(option)
