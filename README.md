# COVID-w-Polsce
![obraz](https://github.com/FlyinButter1/COVID-w-Polsce/assets/85359786/4f84dd61-7af8-4916-8c19-b8e18296b8b5)

## Cel
Celem projektu jest analiza i wizualizacja danych o zakażeniach COVID w Polsce w latach 2020-2022. Pozwala na prześledzenie przebiegu pandemii, wraz z podziałem na województwa.
## Opis rozwiązania
Aplikacja przy wykorzystaniu bilbioteki [pandas](https://github.com/pandas-dev/pandas) scrapeuje dane statystyczne z artykułu na [Wikipedi](https://pl.wikipedia.org/wiki/Statystyki_pandemii_COVID-19_w_Polsce), oczyszcza je, oraz liczy sume zachorowań dla każdego dnia w roku i dla każdego województwa. 

Dokonuje również wizualizacji danych przy użyciu biblioteki [matplotlib](https://github.com/matplotlib/matplotlib). 

Dane przedsatwia w prostej aplikacji internetowej stworzonej przy użyciu biblioteki [flask](https://github.com/pallets/flask). 

Korzystając z biblioteki [pyinstaller](https://github.com/pyinstaller/pyinstaller) projekt zapakowany jest w jeden plik wykonywalny by ułatwic instalację.

## Instalacja
1. Sklonować repozytorium
2. Uruchomimć `docker compose up`

## Lista zależności
Lista zależności znajduje się w pliku [requirements.txt](./requirements.txt)
