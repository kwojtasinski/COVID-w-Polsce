import pandas as pd
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

plt.close("all")

# pobranie tabeli z zakarzeniami w województwach

dfs = pd.read_html("https://pl.wikipedia.org/wiki/Statystyki_pandemii_COVID-19_w_Polsce", match="Zakażenia w województwach w 2021", thousands=" ")
df = dfs[0]

# usunięcie pustych/niepotrzebnych kolumn i wierszy
df.columns = df.columns.droplevel([0, 1])
df = df.iloc[:, :-7]
df = df.drop(df.columns[[1,2,3]], axis=1)
df = df.drop(df.tail(5).index)
df = df.dropna()
df = df.reset_index(drop=True)
df.index += 1

df = df.replace(to_replace = '–', value = 0)

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
plot.set_ylabel("Zakażenia")
plt.savefig('a.png')

plt.close("all")


# generowanie wykresu procentowego udziału województw
s = df.iloc[-1, 1:-1]
s.name = ''
pie = s.plot.pie(autopct='%.1f%%')
plt.savefig('b.png')


# zapisanie w htmlu (do zrobienia strona we flasku)
html = df.to_html() 
  
# write html to file 
text_file = open("index.html", "w") 
text_file.write(html) 
text_file.close() 
