import src.interface.IMarketMan as imm
from src.exchange.mexc.mexc_api_sdk.mexc_sdk.src.mexc_sdk import Spot
from datetime import datetime
import src.exchange.mexc.models.OrderBook as modelOrderBook
import src.exchange.mexc.models.Transaction as modelTransaction
import time
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
            except Exception:
                print('An exeption occured:'+Exception)
                print("l'm going to sleep for 15 seconde")
                time.sleep(15)
            else:
                break
        return modelTransaction.editJsonResponse(response)
    def getKline(self, **d):
        # Implement getKline method for GateMarketMan
        pass   
    def getDepth(self, **d):
        while True:
            try:
                response=self.spot.depth(symbol=d['symbol'],options={'limit':10})
            except Exception:
                print('An exeption occured:'+Exception)
                print("l'm going to sleep for 15 seconde")
                time.sleep(15)
            else:
                break
        return modelOrderBook.editJsonResponse(response)

