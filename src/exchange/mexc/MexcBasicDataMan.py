import src.interface.IBasicDataMan as ibdm
from .api import make_request  
import src.exchange.mexc.models.TradingPairs as modelTradingPairs
import time

class MexcBasicDataMan(ibdm.IBasicDataMan):
    def __init__(self):
        pass

    def getcurrencyPairs(self):
        # Implement the method here
        pass

    def getAccuracyInfo(self):
        while True:
            response = make_request("exchangeInfo")  # Use the new API function
            if response is not None:
                return modelTradingPairs.editJsonResponse(response)
            print("I'm going to sleep for 15 seconds")
            time.sleep(15)
    
    def getRatio(self, **d):
        # Implement the method here
        pass

    def getWithdrawConf(self, **d):
        # Implement the method here
        pass

    def getTimestamp(self):
        # Implement the method here
        pass
