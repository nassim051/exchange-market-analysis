
import src.interface.IBasicDataMan as ibdm
from src.exchange.mexc.mexc_api_sdk.mexc_sdk.src.mexc_sdk import Spot
import src.exchange.mexc.models.TradingPairs as modelTradingPairs

class MexcBasicDataMan(ibdm.IBasicDataMan):
    def __init__(self):
        self.spot=Spot()

    def getcurrencyPairs(self):
        # Implement the method here
        pass

    def getAccuracyInfo(self):
        response=Spot().exchange_info()
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