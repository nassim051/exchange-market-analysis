import time
from src.exchange.gateio.github.gate_api import ApiClient, Configuration
from src.exchange.gateio.github.gate_api.api.spot_api import SpotApi
import src.exchange.gateio.Constants as credential


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
