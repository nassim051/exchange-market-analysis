import src.exchange.mexc.models.Kline as Kline
import src.interface.IMarketMan as imm
from src.exchange.mexc.mexc_api_sdk.mexc_sdk.src.mexc_sdk import Spot
from datetime import datetime
import src.exchange.mexc.models.OrderBook as modelOrderBook
import src.exchange.mexc.models.Transaction as modelTransaction
import time
import json
STANDARD_TIME_TO_MEXC_TIME_MAP = {
'minute1': '1m',
'minute5': '5m',
'minute15': '15m',
'minute30': '30m',
'hour1': '60m',
'hour4': '4h',
'day1': '1d',
'week1': '1W',
'month1': '1M'
}

class MexcMarketMan(imm.IMarketMan):
    def __init__(self):
        self.spot=Spot()

    def getTicker(self, **d):
        # Implement getTicker method for GateMarketMan
        pass
    
    def getIncrDepth(self, **d):
        # Implement getIncrDepth method for GateMarketMan
        pass

    def getTrades(self, **d):
        startTime=int(d['time'])
        endTime=int(datetime.now().timestamp()*1000)
        while True:
            try:
                response=self.spot.agg_trades(symbol=d['symbol'],options={"startTime":startTime,"endTime":endTime})
            except Exception as e:
                print('An exeption occured:'+str(e))
                print("l'm going to sleep for 15 seconde")
                time.sleep(15)
            else:
                print(f"response{response}")
                break
        return modelTransaction.editJsonResponse(response)
    def getKline(self, **d):
        startTime=int(d['time'])
        limit=int(d['size'])

        interval=STANDARD_TIME_TO_MEXC_TIME_MAP[d['type']]

        while True:
            try:
                response=self.spot.klines(symbol=d['symbol'],interval=interval,options={"startTime":startTime,"limit":limit})
            except Exception as e:
                print('An exeption occured:'+str(e))
                print("l'm going to sleep for 15 seconde")
                time.sleep(15)
            else:
                print(f"response{response}")
                break
        return Kline.editJsonResponse(response)
    def getDepth(self, **d):
        while True:
            try:
                response=self.spot.depth(symbol=d['symbol'],options={'limit':10})
            except Exception as e:
                if str(e).__contains__('Invalid symbol.'):
                    print(f"The order book is empty or the bot is not availible for this: {d['symbol']}")
                    return -1
                print('An exeption occured:'+str(e))
                print("l'm going to sleep for 15 seconde")
                time.sleep(15)
            else:
                print(f"response{response}")
                break
        return modelOrderBook.editJsonResponse(response)

