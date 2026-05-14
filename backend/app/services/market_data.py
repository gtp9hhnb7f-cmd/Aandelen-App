from abc import ABC, abstractmethod
from datetime import datetime, timezone
import yfinance as yf


class MarketDataProvider(ABC):
    @abstractmethod
    def get_quotes(self, tickers: list[str]) -> dict:
        ...


class MockMarketDataProvider(MarketDataProvider):
    def get_quotes(self, tickers):
        now = datetime.now(timezone.utc).isoformat()
        return {t: {"price": 100.0 + idx * 5, "currency": "EUR", "timestamp": now, "day_change": 0.5} for idx, t in enumerate(tickers)}


class YahooMarketDataProvider(MarketDataProvider):
    def get_quotes(self, tickers):
        data = {}
        for t in tickers:
            info = yf.Ticker(t).fast_info
            data[t] = {
                "price": float(info.get("lastPrice") or 0),
                "currency": info.get("currency", "EUR"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "day_change": float(info.get("regularMarketChangePercent") or 0),
            }
        return data
