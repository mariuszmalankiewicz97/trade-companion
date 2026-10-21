import json
from pathlib import Path

from trade_companion.daily_trend import DailySetup


def save_h1_watchlist(setups: list[DailySetup], destination_path: Path | str) -> None:
    path = Path(destination_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "count": len(setups),
        "candidates": [setup.to_dict() for setup in setups],
    }

    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def load_h1_watchlist(source_path: Path | str) -> list[DailySetup]:
    path = Path(source_path)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    candidates = data.get("candidates", [])
    return [
        DailySetup(
            ticker=c["ticker"],
            current_close=float(c["current_close"]),
            stop_loss=float(c["stop_loss"]),
            fib_50=float(c["fib_50"]),
            fib_618=float(c["fib_618"]),
            peak_high=float(c["peak_high"]),
        )
        for c in candidates
    ]
