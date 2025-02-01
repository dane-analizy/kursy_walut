import json
from pathlib import Path


def make_filename(year, month, day, currency, rates_dir_name="notowania"):
    """
    Generuje nazwę pliku do przechowywania danych o kursach walut w uporządkowanym katalogu.

    Args:
        year (int): Rok.
        month (int): Miesiąc.
        day (int): Dzień.
        currency (str): Kod waluty (np. 'USD', 'EUR').
        rates_dir_name (str, optional): Nazwa głównego katalogu do przechowywania kursów. Domyślnie "notowania".

    Returns:
        Path: Obiekt Path reprezentujący pełną ścieżkę do wygenerowanej nazwy pliku.
    """

    # katalogi
    # bieżący katalog
    current_dir = Path()
    # katalog główny do przechowywania kursów
    rates_dir = current_dir / rates_dir_name.lower()
    # tworzenie katalogu głównego, jeśli nie istnieje
    rates_dir.mkdir(exist_ok=True)
    # katalog dla danej waluty
    currency_dir = rates_dir / currency.lower()
    # tworzenie katalogu dla waluty, jeśli nie istnieje
    currency_dir.mkdir(exist_ok=True)

    # nazwa pliku
    return currency_dir / f"{year:04}_{month:02}_{day:02}.json"


def save_data_to_file(data, file_name):
    """
    Zapisuje dane do pliku w formacie JSON.

    Args:
        data (dict): Dane do zapisania w pliku.
        file_name (str): Ścieżka do pliku, w którym dane mają być zapisane.

    Raises:
        IOError: Jeśli wystąpi błąd podczas zapisywania pliku.
    """
    
    with open(file_name, "w", encoding="utf-8") as fp:
        json.dump(data, fp)
