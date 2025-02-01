import yaml


def load_config(file_path="config.yaml"):
    """
    Ładuje konfigurację z pliku YAML.

    Args:
        file_path (str): Ścieżka do pliku konfiguracyjnego YAML. Domyślnie "config.yaml".

    Returns:
        dict: Zawartość pliku konfiguracyjnego jako słownik.

    Raises:
        FileNotFoundError: Jeśli plik nie zostanie znaleziony.
        yaml.YAMLError: Jeśli wystąpi błąd podczas parsowania pliku YAML.
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
