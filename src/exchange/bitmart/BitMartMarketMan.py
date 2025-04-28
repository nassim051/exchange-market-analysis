import src.interface.IMarketMan as imm
from bitmart.api_spot import APISpot as SpotClient

from bitmart.lib import cloud_exceptions
import time
from types import SimpleNamespace

class BitMartMarketMan(imm.IMarketMan):
    def __init__(self):
        self.client = SpotClient()

    def getDepth(self, **d):
        try:
            result = self.client.get_v3_depth(d["symbol"], limit=50)[0]
            asks = [(float(x[0]), float(x[1])) for x in result['data']['asks']]
            bids = [(float(x[0]), float(x[1])) for x in result['data']['bids']]
            return SimpleNamespace(asks=asks, bids=bids)
        except Exception as e:
            print(f"[BitMart] Error fetching depth: {e}")
            return -1
    def getTrades(self, **d):
        try:
            limit = d.get('size', 50)
            result = self.client.get_v3_trades(symbol=d["symbol"], limit=limit)[0]
            trades = []
            print(f"Trades: {result['data'][0]}")

            for trade in result['data']:
                trades.append(SimpleNamespace(
                    price=float(trade[2]),
                    qty=float(trade[3]),
                    time=int(trade[1]) 
                ))
            return trades
        except cloud_exceptions.APIException as e:
            print(f"[BitMart] Error fetching trades: {e}")
            return []

    def getKline(self, **d):
        try:
            limit = d.get("limit", d.get("size", 100))
            time_from = int(d["time"]) if "time" in d else int(time.time())
            interval = self.map_interval(d["type"])
            result = self.client.get_v3_history_kline(
                symbol=d["symbol"],
                step=interval,
                after=time_from,
                limit=limit
            )[0]
            klines = []
            for k in result["data"]:
                klines.append(SimpleNamespace(
                    time=int(k[0]),
                    open=float(k[1]),
                    high=float(k[3]),
                    low=float(k[4]),
                    close=float(k[2]),
                    volume=float(k[5])
                ))
            return klines
        except cloud_exceptions.APIException as e:
            print(f"[BitMart] Error fetching kline: {e}")
            return []

    def getTicker(self, **d):
        # Optional if needed
        pass

    def getIncrDepth(self, **d):
        # Not supported on BitMart
        pass

    def map_interval(self, tf):
        map_ = {
            "minute1": "1",
            "minute5": "5",
            "minute15": "15",
            "minute30": "30",
            "hour1": "60",
            "hour4": "240",
            "hour8": "480",
            "hour12": "720",
            "day1": "1D",
            "week1": "1W",
            "month1": "1M"
        }
        return map_.get(tf, "60")
