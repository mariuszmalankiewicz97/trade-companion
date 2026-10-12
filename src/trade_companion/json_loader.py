import json
from pathlib import Path


def json_loader(path: Path | str) -> dict:
    try:
        extension = Path(path).suffix
        if extension != ".json":
            raise ValueError("File must have .json extension")
        with open(path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    else:
        return data
