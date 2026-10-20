import json
from itertools import chain
from pathlib import Path


def extract_tickers(data: dict) -> list[str]:
    """Wyciąga unikalne tickery ze słownika, zachowując kolejność wystąpienia."""
    if not isinstance(data, dict):
        raise TypeError("Type must be a dict")
    if not data:
        raise ValueError("Missing tickers")

    all_tickers = chain.from_iterable(data.values())
    # dict.fromkeys usuwa duplikaty i zachowuje kolejność (w przeciwieństwie do set)
    return list(dict.fromkeys(all_tickers))


def load_tickers(path: Path | str) -> list[str]:
    """Wczytuje plik konfiguracyjny JSON i zwraca wyczyszczoną listę tickerów."""
    file_path = Path(path)

    if file_path.suffix != ".json":
        raise ValueError("File must have .json extension")

    # Path.open rzuca naturalny FileNotFoundError z pełną ścieżką do pliku
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return extract_tickers(data)
