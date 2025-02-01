from utils.config import load_config
from utils.db import close_db, make_db_table, open_db, save_data_to_db
from utils.files import make_filename, save_data_to_file
from utils.utils import generate_dates
from utils.web import get_rates

CONFIG_FILE = "config.yaml"


def main():
    # Załaduj konfigurację z pliku YAML
    config = load_config(CONFIG_FILE)

    # Wygeneruj listę dat, dla których mają być pobrane kursy
    rate_dates = generate_dates(config["start_date"])

    # Otwórz połączenie z bazą danych, jeśli zapisywanie do bazy danych jest włączone
    if config["save_to_db"]:
        db = open_db(config)
        make_db_table(db)

    # Przejdź przez każdą datę, aby pobrać i przetworzyć kursy
    for date in rate_dates:
        req_year, req_month, req_day = date  # Rozpakuj krotkę na trzy zmienne
        nbp_rates = get_rates(
            req_year, req_month, req_day, expected_currencies=config["currencies"]
        )

        # Przetwórz każdy kurs waluty
        for currency in nbp_rates:
            currency_code = currency["code"]
            filename = make_filename(
                req_year,
                req_month,
                req_day,
                currency_code,
                rates_dir_name=config["output_folder"],
            )

            # Zapisz dane do pliku, jeśli jest to włączone w konfiguracji
            if config["save_to_file"]:
                save_data_to_file(currency, filename)

            # Zapisz dane do bazy danych, jeśli jest to włączone w konfiguracji
            if config["save_to_db"]:
                save_data_to_db(currency, db)

    # Zamknij połączenie z bazą danych
    close_db(db)


if __name__ == "__main__":
    main()
