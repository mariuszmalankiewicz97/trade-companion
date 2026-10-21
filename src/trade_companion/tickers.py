import json
from itertools import chain
from pathlib import Path


def extract_tickers(data: dict) -> list[str]:
    if not isinstance(data, dict):
        raise TypeError("Type must be a dict")
    if not data:
        raise ValueError("Missing tickers")

    raw_tickers = chain.from_iterable(data.values())

    cleaned = [
        item.strip().upper()
        for item in raw_tickers
        if isinstance(item, str) and item.strip()
    ]

    if not cleaned:
        raise ValueError("No valid tickers found in data")

    return list(dict.fromkeys(cleaned))


def load_tickers(path: Path | str) -> list[str]:
    file_path = Path(path)

    if file_path.suffix != ".json":
        raise ValueError("File must have .json extension")

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return extract_tickers(data)
