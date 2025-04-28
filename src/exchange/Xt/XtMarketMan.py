from types import SimpleNamespace
import time
from pyxt.spot import Spot
from src.interface.IMarketMan import IMarketMan

STANDARD_TIME_TO_XT_TIME_MAP = {
    'minute1': '1m',
    'minute5': '5m',
    'minute15': '15m',
    'minute30': '30m',
    'hour1': '1h',
    'hour4': '4h',
    'hour8': '8h',
    'hour12': '12h',
    'day1': '1d',
    'week1': '7d',
    'month1': '30d'
}
INTERVAL_TO_MS = {
    "1m": 60 * 1000,
    "3m": 3 * 60 * 1000,
    "5m": 5 * 60 * 1000,
    "15m": 15 * 60 * 1000,
    "30m": 30 * 60 * 1000,
    "1h": 60 * 60 * 1000,
    "2h": 2 * 60 * 60 * 1000,
    "4h": 4 * 60 * 60 * 1000,
    "6h": 6 * 60 * 60 * 1000,
    "8h": 8 * 60 * 60 * 1000,
    "12h": 12 * 60 * 60 * 1000,
    "1d": 24 * 60 * 60 * 1000,
    "3d": 3 * 24 * 60 * 60 * 1000,
    "1w": 7 * 24 * 60 * 60 * 1000,
    "1M": 30 * 24 * 60 * 60 * 1000  # Approximate 1 month = 30 days
}
class XtMarketMan(IMarketMan):
    def __init__(self):
        self.client =  Spot(host="https://sapi.xt.com", access_key='', secret_key='')

    def getTicker(self, **d):
        pass  # Implement if needed

    def getIncrDepth(self, **d):
        pass  # Not used for now

    def getDepth(self, **d):
        symbol = d.get("symbol")
        if not symbol:
            raise KeyError("Symbol is required")

        while True:
            try:
                response = self.client.get_depth(symbol=symbol, limit=d.get("limit", 100))
                return SimpleNamespace(
                    asks=[[float(i[0]), float(i[1])] for i in response['asks']],
                    bids=[[float(i[0]), float(i[1])] for i in response['bids']]
                )
            except Exception as e:
                print(f"Error in getDepth: {e}, for symbol: {symbol}")
                return -1




    def getTrades(self, **d):

        symbol = d.get("symbol")
        if not symbol:
            raise KeyError("Symbol is required")

        start_time = float(d.get("time"))  # in ms
        size = d.get("size", 100)
        trades = []
        try:
            recent = self.client.get_trade_recent(symbol=symbol, limit=size)
            print("[XT] Fetched recent trades.")
            
            oldest_recent = float(recent[-1]["t"])
            if oldest_recent <= start_time:
                print("All transaction timestamps are newer than the specified time.")
            else:
                print("Old transaction are still missing.")

            return [
                SimpleNamespace(
                    time=float(trade["t"]),
                    price=float(trade["p"]),
                    qty=float(trade["q"]),
                    is_buyer_maker=trade.get("b", False),
                )
                for trade in recent
                if float(trade["t"]) >= start_time
            ]


        except Exception as e:
            print(f"[XT] Error in getTrades: {e}, for symbol: {symbol}")

            return []

    def getKline(self, **d):
        symbol = d.get("symbol")
        if not symbol:
            raise KeyError("Symbol is required")
        
        interval = STANDARD_TIME_TO_XT_TIME_MAP.get(d.get("type", "hour1"), "1h")
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": d.get("size", 1000)
        }

        now_ms = int(time.time() * 1000)
        start_time_ms = d.get("time")
        interval_ms = INTERVAL_TO_MS.get(interval)

        if start_time_ms and interval_ms:
            elapsed_ms = now_ms - start_time_ms
            size = max(1, elapsed_ms // interval_ms)  # minimum 1
            params["limit"] = int(size)

        try:
            response = self.client.get_kline(**params)

            # Reverse because XT.com returns newest ➔ oldest
            response = list(reversed(response))

            klines = [SimpleNamespace(
                time=float(k['t']),
                open=float(k['o']),
                high=float(k['h']),
                low=float(k['l']),
                close=float(k['c']),
                volume=float(k['v'])
            ) for k in response]

            if klines:
                # HACK: duplicate the last kline with actual current time
                last_kline = klines[-1]
                now_ms = int(time.time() * 1000)
                fake_kline = SimpleNamespace(
                    time=float(now_ms),
                    open=last_kline.open,
                    high=last_kline.high,
                    low=last_kline.low,
                    close=last_kline.close,
                    volume=last_kline.volume
                )
                klines.append(fake_kline)

            return klines

        except Exception as e:
            print(f"Error in getKline: {e}, symbol: {symbol}, params: {params}")
            return []

