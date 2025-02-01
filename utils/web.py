from datetime import datetime

import requests


def make_query_url(year, month, day, table="A"):
    """
    Tworzy URL zapytania do API NBP dla podanej daty i tabeli kursów walut.

    Args:
        year (int): Rok w formacie czterocyfrowym.
        month (int): Miesiąc w formacie dwucyfrowym.
        day (int): Dzień w formacie dwucyfrowym.
        table (str, opcjonalnie): Typ tabeli kursów walut (domyślnie "A").

    Returns:
        str: URL zapytania do API NBP w formacie JSON.
    """

    return f"https://api.nbp.pl/api/exchangerates/tables/{table}/{year:04}-{month:02}-{day:02}/?format=json"


def get_rates(
    year, month, day, table="A", expected_currencies=["eur", "usd", "gbp", "chf"]
):
    """
    Pobiera kursy walut z tabeli NBP dla podanej daty.

    Args:
        year (int): Rok, dla którego mają być pobrane kursy.
        month (int): Miesiąc, dla którego mają być pobrane kursy.
        day (int): Dzień, dla którego mają być pobrane kursy.
        table (str, optional): Typ tabeli NBP (domyślnie "A").
        expected_currencies (list, optional): Lista oczekiwanych walut (domyślnie ["eur", "usd", "gbp", "chf"]).

    Returns:
        list: Lista słowników zawierających kursy oczekiwanych walut. Każdy słownik zawiera klucze "code", "currency", "mid" oraz "data".
              Jeśli wystąpi błąd, zwraca pustą listę.
    """
    
    # Konwertuje oczekiwane waluty na małe litery
    expected_currencies_lower = [element.lower() for element in expected_currencies]

    # Tworzy URL zapytania do API NBP
    query_url = make_query_url(year, month, day, table)
    result = requests.get(query_url)

    # Sprawdza, czy zapytanie zakończyło się sukcesem
    if result.status_code != 200:
        return []

    # Pobiera tabelę kursów z odpowiedzi
    table = result.json()[0]
    rates = table.get("rates", [])

    # Filtruje kursy, aby zawierały tylko oczekiwane waluty
    rates_filtered = [
        rate for rate in rates if rate["code"].lower() in expected_currencies_lower
    ]

    # Dodaje datę do każdego kursu
    data = datetime(year, month, day).date().strftime("%Y-%m-%d")
    for rate in rates_filtered:
        rate.update({"data": data})

    # Zwraca przefiltrowane kursy
    return rates_filtered
