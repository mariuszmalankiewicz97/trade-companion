from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class DailySetup:
    ticker: str
    current_close: float
    stop_loss: float
    fib_50: float
    fib_618: float
    peak_high: float

    def to_dict(self) -> dict:
        return asdict(self)


@runtime_checkable
class DataProvider(Protocol):
    def fetch_data(self, ticker: str, period: str, interval: str) -> list[Candle]: ...
