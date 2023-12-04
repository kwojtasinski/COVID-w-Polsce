import pandas as pd
pd.options.mode.chained_assignment = None

# pobranie tabeli z zakarzeniami w województwach

dfs = pd.read_html("https://pl.wikipedia.org/wiki/Statystyki_pandemii_COVID-19_w_Polsce", match="Zakażenia w województwach w 2021")
df = dfs[0]

# usunięcie pustych/niepotrzebnych kolumn i wierszy
df = df.iloc[:, :-7]
df = df.drop(df.columns[[1,2,3]], axis=1)
df = df.drop(df.tail(5).index)
df = df.dropna()

# zapisanie w htmlu (do zrobienia strona we flasku)

html = df.to_html() 
  
# write html to file 
text_file = open("index.html", "w") 
text_file.write(html) 
text_file.close() 
