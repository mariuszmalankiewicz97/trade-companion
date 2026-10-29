import yfinance as yf

from trade_companion.models import Candle


class YFinanceProvider:
    def fetch_data(self, ticker: str, period: str, interval: str) -> list[Candle]:
        df = yf.download(ticker, period=period, interval=interval)

        candles = []
        for index, row in df.iterrows():
            candle = Candle(
                open=row["Open"],
                high=row["High"],
                low=row["Low"],
                close=row["Close"],
                volume=row["Volume"],
                timestamp=index,
            )
            candles.append(candle)

        return candles
