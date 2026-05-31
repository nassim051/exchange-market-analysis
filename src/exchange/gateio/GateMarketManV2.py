import time
from src.exchange.gateio.github.gate_api import ApiClient, Configuration
from src.exchange.gateio.github.gate_api.api.spot_api import SpotApi
import src.exchange.gateio.Constants as credential
import pandas as pd
from datetime import datetime, timezone, timedelta



class GateIoMarketManV2:
    def __init__(self, max_retries=5, retry_delay=15):
        config = Configuration(key=credential.key, secret=credential.secret)
        self.api = SpotApi(ApiClient(config))
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _retry(self, func, *args, **kwargs):
        retries = 0
        while retries < self.max_retries:
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                print(f"[GateIoMarketManV2] Error: {e}, retrying in {self.retry_delay}s...")
                time.sleep(self.retry_delay)
                retries += 1
        raise Exception(f"[GateIoMarketManV2] Failed after {self.max_retries} retries.")

    # === Wrappers below: ===

    def get_currency_pair(self, symbol):
        return self._retry(self.api.get_currency_pair, currency_pair=symbol)

    def list_candlesticks(self, currency_pair, interval, limit):
        return self._retry(
            self.api.list_candlesticks,
            currency_pair=currency_pair,
            interval=interval,
            limit=limit
        )

    def list_order_book(self, currency_pair, limit=100):
        return self._retry(
            self.api.list_order_book,
            currency_pair=currency_pair,
            limit=limit
        )

    def list_tickers(self, currency_pair):
        return self._retry(
            self.api.list_tickers,
            currency_pair=currency_pair
        )

    def create_order(self, order):
        return self._retry(
            self.api.create_order,
            order=order
        )

    def cancel_order(self, order_id, currency_pair):
        return self._retry(
            self.api.cancel_order,
            order_id=order_id,
            currency_pair=currency_pair
        )

    def get_order(self, order_id, currency_pair):
        return self._retry(
            self.api.get_order,
            order_id=order_id,
            currency_pair=currency_pair
        )



    def get_full_ohlcv_dataframe(self, currency_pair, interval, start, end):
        """
        Fetch full OHLCV data for a symbol from `start` to `end`, split into 1000-candle chunks.

        Args:
            currency_pair (str): e.g. "BTC_USDT"
            interval (str): e.g. "1m", "1h"
            start (datetime): UTC datetime start
            end (datetime): UTC datetime end

        Returns:
            pd.DataFrame: Clean OHLCV DataFrame (index=datetime)
        """

        # Gate.io interval to seconds
        interval_seconds = {
            "1m": 60, "5m": 300, "15m": 900, "30m": 1800,
            "1h": 3600, "4h": 14400, "1d": 86400
        }[interval]

        start_ts = int(start.replace(tzinfo=timezone.utc).timestamp())
        end_ts = int(end.replace(tzinfo=timezone.utc).timestamp())

        all_rows = []

        while start_ts < end_ts:
            to_ts = min(start_ts + 1000 * interval_seconds - 1, end_ts)

            chunk = self._retry(
                self.api.list_candlesticks,
                currency_pair=currency_pair,
                interval=interval,
                _from=start_ts,
                to=to_ts,
                limit=1000
            )

            if not chunk:
                break

            for row in chunk:
                all_rows.append({
                    "timestamp": int(row[0]),
                    "volume": float(row[1]),
                    "close": float(row[2]),
                    "high": float(row[3]),
                    "low": float(row[4]),
                    "open": float(row[5])
                })

            # Next chunk start
            start_ts = int(all_rows[-1]["timestamp"]) + interval_seconds

        # Build DataFrame
        if not all_rows:
            return pd.DataFrame()

        df = pd.DataFrame(all_rows)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
        df.set_index("timestamp", inplace=True)
        df = df[["open", "high", "low", "close", "volume"]].sort_index()
        return df
