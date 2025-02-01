from datetime import datetime, timedelta

from flask import Flask, render_template
from utils.config import load_config
from utils.db import close_db, currency_lists_from_db, load_data_from_db, open_db

CONFIG_FILE = "config.yaml"

# załaduj konfigurację z pliku YAML
config = load_config(CONFIG_FILE)

# zbuduj obiekt aplikacji Flask
app = Flask("Notowania kursów NBP")


@app.route("/")  # brak jakichkolwiek parametrow
@app.route("/kurs")  # brak jakichkolwiek parametrow
@app.route("/kurs/<waluta>")  # tylko waluta
@app.route("/kurs/<waluta>/<data_od>")  # tylko waluta i data od
@app.route("/kurs/<waluta>/<data_od>/<data_do>")  # komplet parametrow
def kurs(waluta="EUR", data_od=None, data_do=None):
    # dziś
    today = datetime.now()
    # 30 dni temu
    today_30_days_ago = today - timedelta(days=30)

    # jeśli brakuje argumentow - użyj wyliczonych dat
    if not data_od:
        data_od = today_30_days_ago.strftime("%Y-%m-%d")
    if not data_do:
        data_do = today.strftime("%Y-%m-%d")

    # podłaczenie do bazy - z konfiguracji będzie wiadomo co to za baza i gdzie leży
    db = open_db(config)

    # lista dostępnych walut (dla jakich walut mamy zgromadzone notowania)
    currencies = currency_lists_from_db(db)
    # pobranie notowań dla konkretnej waluty w konkretnym zakresie dat
    results = load_data_from_db(db, waluta, data_od, data_do)

    # zamkniecie połaczenia z baza
    close_db(db)

    # wstawienie danych do szablonu
    return render_template(
        "rates.html",
        data=results,
        currencies=currencies,  # lista dostepnych walut
        current_currency=waluta,  # aktualnie wybrana waluta
        selected_date_from=data_od,
        selected_date_to=data_do,
    )


if __name__ == "__main__":
    # host = 0.0.0.0 oznacza, że z każdej maszyny można pytać naszą aplikację
    # aplikacja nasłuchuje na porcie 5000
    app.run(host="0.0.0.0", port=5000)
