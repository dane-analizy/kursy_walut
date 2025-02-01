from sqlalchemy import create_engine, text


def make_connection_string(config):
    """
    Tworzy string połączenia do bazy danych na podstawie podanej konfiguracji.

    Args:
        config (dict): Słownik zawierający konfigurację połączenia do bazy danych.
                       Powinien zawierać klucze:
                       - "db_type" (str): Typ bazy danych, np. "sqlite" lub "postgresql".
                       - "sqlite_database_file" (str): Ścieżka do pliku bazy danych SQLite (jeśli db_type to "sqlite").
                       - "db_user" (str): Nazwa użytkownika bazy danych (jeśli db_type to "postgresql").
                       - "db_pass" (str): Hasło użytkownika bazy danych (jeśli db_type to "postgresql").
                       - "db_host" (str): Adres hosta bazy danych (jeśli db_type to "postgresql").
                       - "db_port" (str): Port bazy danych (jeśli db_type to "postgresql").
                       - "db_name" (str): Nazwa bazy danych (jeśli db_type to "postgresql").

    Returns:
        str: String połączenia do bazy danych. Zwraca pusty string, jeśli typ bazy danych nie jest obsługiwany.
    """
    
    if config["db_type"] == "sqlite":
        # Tworzenie stringa połączenia dla SQLite
        conn_str = f"sqlite:///{config['sqlite_database_file']}"
    elif config["db_type"] == "postgresql":
        # Tworzenie stringa połączenia dla PostgreSQL
        conn_str = f"postgresql+psycopg2://{config['db_user']}:{config['db_pass']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
    else:
        # Zwraca pusty string, jeśli typ bazy danych nie jest obsługiwany
        conn_str = ""
    return conn_str


def open_db(config):
    """
    Otwiera połączenie z bazą danych na podstawie podanej konfiguracji.

    Args:
        config (dict): Słownik zawierający parametry konfiguracji bazy danych.

    Returns:
        db_conn: Obiekt połączenia z bazą danych.
    """

    # Tworzy string połączenia do bazy danych na podstawie konfiguracji
    connection_str = make_connection_string(config)
    # Tworzy silnik bazy danych
    db_engine = create_engine(connection_str)
    # Otwiera połączenie z bazą danych
    db_conn = db_engine.connect()
    # Zwraca obiekt połączenia z bazą danych
    return db_conn


def close_db(db):
    """Zamyka połączenie z bazą danych."""
    db.close()


def make_db_table(db_conn):
    """Tworzy tabelę 'rates' w bazie danych, jeśli taka tabela nie istnieje.

    Tabela 'rates' zawiera następujące kolumny:
    - data: typ DATE, nie może być NULL
    - currency_code: typ VARCHAR, nie może być NULL
    - exchange_rate: typ FLOAT, nie może być NULL

    Klucz główny (PRIMARY KEY) składa się z kolumn 'data' i 'currency_code'.

    Args:
        db_conn (sqlalchemy.engine.Connection): Połączenie do bazy danych, na którym zostanie wykonane zapytanie SQL."""
    
    # Definiuje zapytanie SQL do utworzenia tabeli 'rates', jeśli taka tabela nie istnieje
    query = """
        CREATE TABLE IF NOT EXISTS rates (
            data DATE NOT NULL,
            currency_code VARCHAR NOT NULL,
            exchange_rate FLOAT NOT NULL,
            PRIMARY KEY (data, currency_code)
        );
    """
    # Wykonuje zapytanie SQL na połączeniu z bazą danych
    db_conn.execute(text(query))


def save_data_to_db(currency, db_conn):
    """Zapisuje dane walutowe do bazy danych.

    Args:
        currency (dict): Słownik zawierający dane walutowe, w tym klucze 'data', 'code' i 'mid'.
        db_conn (Connection): Obiekt połączenia z bazą danych.

    Raises:
        Exception: W przypadku błędu podczas wykonywania zapytania INSERT."""
    insert_query = """
    INSERT INTO rates (data, currency_code, exchange_rate) 
    VALUES (:data, :code, :mid);
    """

    ## sprobuj wstawic dane do bazy
    try:
        ## slownik notowanie jako paczka parametrow
        db_conn.execute(text(insert_query), currency)
        db_conn.commit()
    except Exception as e:
        print(f"Blad przy INSERT:\n{e}")


def load_data_from_db(db_conn, currency, start_date, end_date):
    """Ładuje dane z bazy danych dla określonej waluty w zadanym przedziale czasowym.

    Args:
        db_conn (Connection): Połączenie do bazy danych.
        currency (str): Kod waluty (np. 'USD', 'EUR').
        start_date (str): Data początkowa w formacie 'YYYY-MM-DD'.
        end_date (str): Data końcowa w formacie 'YYYY-MM-DD'.

    Returns:
        list: Lista słowników zawierających daty i kursy walut w zadanym przedziale czasowym.
            Każdy słownik ma klucze 'date' i 'rate'.
            Jeśli wystąpi błąd, zwraca pustą listę.
    """

    ## parametry dla zapytania
    params = {
        "currency": currency.upper(),  # parametr moze byc malymi literami, w bazie mamy duze
        "start_date": start_date,
        "end_date": end_date,
    }

    ## zapytanie
    query = """
        SELECT
            data, exchange_rate
        FROM rates
        WHERE
            currency_code = :currency
            AND data >= :start_date
            AND data <= :end_date
        ORDER BY
            data ASC;
    """

    ## sprobuj pobrac dane z bazy
    try:
        db_results = db_conn.execute(text(query), params)
    except Exception as e:
        ## nie udalo sie to wypisz blad i zwroc pusta liste
        print(f"Blad pobrania kwotowan:\n{e}")
        return []

    ## wyniki z bazy przepisujemy na liste slownikow
    results = []
    for r in db_results:
        ## element [0] = data, [1] = kurs
        results.append({"date": r[0], "rate": r[1]})

    return results


def currency_lists_from_db(db_conn):
    """Pobiera listę unikalnych kodów walut z bazy danych.
    Funkcja wykonuje zapytanie SQL, aby pobrać unikalne kody walut z tabeli 'rates'
    i zwraca je w postaci listy. W przypadku niepowodzenia zapytania, funkcja
    wypisuje błąd i zwraca pustą listę.

    Args:
        db_conn (SQLAlchemy Connection): Połączenie do bazy danych.

    Returns:
        list: Lista unikalnych kodów walut w postaci stringów. W przypadku błędu zwraca pustą listę.
    """

    query = """
        SELECT DISTINCT currency_code
        FROM rates
        ORDER BY currency_code ASC;
    """

    ## sprobuj pobrac dane z bazy
    try:
        db_results = db_conn.execute(text(query))
    except Exception as e:
        ## nie udalo sie to wypisz blad i zwroc pusta liste
        print(f"Blad pobrania listy walut:\n{e}")
        return []

    ## wyniki z bazy przepisujemy na liste
    results = [r[0] for r in db_results]

    return results
