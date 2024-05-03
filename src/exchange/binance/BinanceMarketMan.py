import src.interface.IMarketMan as imm
from src.exchange.binance.binance_git.binance.spot import Spot
from datetime import datetime
import src.exchange.binance.models.Kline as kline
import time
STANDARD_TIME_TO_BINANCE_TIME_MAP = {
'minute1': '1m',
'minute5': '5m',
'minute15': '15m',
'minute30': '30m',
'hour1': '1h',
'hour4': '4h',
'hour8': '8h',
'hour12': '12h',
'day1': '1d',
'week1': '1w',
'month1': '1M'
}
class BinanceMarketMan(imm.IMarketMan):

    def __init__(self):
        self.spot=Spot()

    def getTicker(self, **d):
        # Implement getTicker method for GateMarketMan
        pass
    
    def getIncrDepth(self, **d):
        # Implement getIncrDepth method for GateMarketMan
        pass

    def getTrades(self, **d):
        pass
    def getKline(self, **d):
        while True:
            try:
                result=self.spot.klines(limit=d['size'],symbol=d['symbol'],startTime=int(d['time']),interval=STANDARD_TIME_TO_BINANCE_TIME_MAP[d['type']])
            except Exception as e:
                    print(f"Following exception occured: {e}")
                    if hasattr(e, 'status_code') and e.status_code==429:
                        print("Will sleep for 4 minutes")
                        time.sleep(60*4)
                    else:
                        print("Will sleep for 15 secondes")
                        time.sleep(15)
            else:
                break
        return kline.editJsonResponse(result)
    def getDepth(self, **d):
       pass