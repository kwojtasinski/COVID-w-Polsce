import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

pd.options.mode.chained_assignment = None

plt.close("all")


def generate_latest():
    return pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/latest/owid-covid-latest.csv")

def generate_table(year):
    # pobranie tabeli z zakarzeniami w województwach

    
    dfs = pd.read_html("https://pl.wikipedia.org/wiki/Statystyki_pandemii_COVID-19_w_Polsce", match=f"Zakażenia w województwach w {year}", thousands=" ")
    df = dfs[0]


    # usunięcie pustych/niepotrzebnych kolumn i wierszy
    df.columns = df.columns.droplevel([0, 1])
    df = df.iloc[:, :-7]
    df = df.drop(df.columns[[1,2,3]], axis=1)
    df = df.drop(df.tail(5).index)
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.index += 1

    if(year == '2022'):
        df.columns = df.columns.droplevel([1])
        df = df[df['pomorskie'].str.contains("2022") == False]

    # dwa rodzaje używanych myślników
    df.replace(to_replace = '–', value = 0, inplace=True)
    df.replace(to_replace = '-', value = 0, inplace=True)


    #zamiana typu danych 
    for column in df.columns:
        if column == "Data":
            continue
        df[column] = df[column].astype(int)

    # dodanie kolumny i wiersza z sumowaniem
    df.loc[:, "Total"] = df.sum(numeric_only=True ,axis= 1)
    df.loc["Total"] = df.sum(numeric_only=True ,axis= 0)

    #znowu zmiana typu danych na int (zmieniaja sie na float?) 
    for column in df.columns:
        if column == "Data":
            continue
        df[column] = df[column].astype(int)


    # # generowanie wykresu zakarzeń w skali roku
    # plot = df.drop(df.tail(1).index).plot(y="Total")
    # plot.set_xlabel("Dni roku")
    # plot.set_ylabel("Nowe zakażenia")
    # plt.savefig(f'static/{year}-1.png')

    # plt.close("all")


    # generowanie wykresu procentowego udziału województw
    s = df.iloc[-1, 1:-1]
    s.name = ''
    pie = s.plot.pie(autopct='%.1f%%')


    return df

# generate_table('2020')
# generate_table('2021')
# generate_table('2022')



option = st.selectbox("Wybierz rok",
                      pd.Series(["Latest worldwide", "Poland 2020", "Poland 2021", "Poland 2022"]))


if option == "Latest worldwide":
    df = generate_latest()
    st.write(df)
else:
    df = generate_table(option[7:])
    st.write(df)
    st.line_chart(df[:-1], y="Total", use_container_width=True)
    st.pyplot(plt)
