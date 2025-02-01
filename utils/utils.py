from datetime import datetime, timedelta


def generate_dates(start_date):
    """
    Generuje listę dat od podanej daty początkowej do dzisiejszej daty.

    Args:
        start_date (str lub datetime.date): Data początkowa w formacie 'YYYY-MM-DD' lub jako obiekt datetime.date.

    Returns:
        list: Lista krotek, gdzie każda krotka zawiera rok, miesiąc i dzień (year, month, day) dla każdej daty od start_date do dzisiejszej daty.
    """
    
    # Konwersja stringa na obiekt daty
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    # Pobranie dzisiejszej daty
    end_date = datetime.now().date()

    # Lista na wynikowe daty
    date_list = []

    # Generowanie dat
    current_date = start_date
    while current_date <= end_date:
        date_list.append((current_date.year, current_date.month, current_date.day))
        current_date += timedelta(days=1)

    return date_list
