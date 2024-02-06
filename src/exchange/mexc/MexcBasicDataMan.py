
import src.interface.IBasicDataMan as ibdm
from src.exchange.mexc.mexc_api_sdk.mexc_sdk.src.mexc_sdk import Spot
import src.exchange.mexc.models.TradingPairs as modelTradingPairs
import time
class MexcBasicDataMan(ibdm.IBasicDataMan):
    def __init__(self):
        self.spot=Spot()

    def getcurrencyPairs(self):
        # Implement the method here
        pass

    def getAccuracyInfo(self):
        while True:
            try:
                response=Spot().exchange_info()    
            except Exception as e:
                print('An exeption occured:'+str(e))
                print("l'm going to sleep for 15 seconde")
                time.sleep(15)
            else:
                break
        return modelTradingPairs.editJsonResponse(response)
    
    def getRatio(self, **d):
        # Implement the method here
        pass

    def getWithdrawConf(self, **d):
        # Implement the method here
        pass

    def getTimestamp(self):
        # Implement the method here
        pass