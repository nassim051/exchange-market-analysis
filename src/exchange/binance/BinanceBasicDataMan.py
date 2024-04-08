
import src.interface.IBasicDataMan as ibdm
from src.exchange.binance.binance_git.binance.spot import Spot

import time
class BinanceBasicDataMan(ibdm.IBasicDataMan):
    def __init__(self):
        self.spot=Spot()

    def getcurrencyPairs(self):
        # Implement the method here
        pass

    def getAccuracyInfo(self):
        while True:
            try:
                result=self.spot.exchange_info()
            except Exception as e:
                    print(f"Following exception occured: {e}")
                    print("Will sleep for 15 secondes")
                    time.sleep(15)
            else:
                break
        return result
    
    def getRatio(self, **d):
        # Implement the method here
        pass

    def getWithdrawConf(self, **d):
        # Implement the method here
        pass

    def getTimestamp(self):
        # Implement the method here
        pass