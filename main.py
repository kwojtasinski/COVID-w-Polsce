import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, url_for, request, render_template

pd.options.mode.chained_assignment = None

plt.close("all")


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


    # generowanie wykresu zakarzeń w skali roku
    plot = df.drop(df.tail(1).index).plot(y="Total")
    plot.set_xlabel("Dni roku")
    plot.set_ylabel("Nowe zakażenia")
    plt.savefig(f'static/{year}-1.png')

    plt.close("all")


    # generowanie wykresu procentowego udziału województw
    s = df.iloc[-1, 1:-1]
    s.name = ''
    pie = s.plot.pie(autopct='%.1f%%')
    plt.savefig(f'static/{year}-2.png')


    # zapisanie w htmlu
    html = df.to_html()
    text_file = open(f"templates/{year}.html", "w") 
    text_file.write(html) 
    text_file.close() 

generate_table('2020')
generate_table('2021')
generate_table('2022')


app = Flask("app", static_folder='static', template_folder="templates", static_url_path="/")

@app.route("/")
def index():
    if('year' in request.args):
        #render.html
        year = request.args['year']
        return render_template("render.html", year=year)
    else:
        return render_template("main.html")
    
app.run()