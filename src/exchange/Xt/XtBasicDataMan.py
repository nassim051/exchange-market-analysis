# src/exchange/xt/XtBasicDataMan.py
from src.interface.IBasicDataMan import IBasicDataMan
import time
from pyxt.spot import Spot
from types import SimpleNamespace

class XtBasicDataMan(IBasicDataMan):
    def __init__(self):
        self.client =  Spot(host="https://sapi.xt.com", access_key='', secret_key='')


    def getcurrencyPairs(self):
        pass  # Not required


    def getAccuracyInfo(self):
        while True:
            try:
                response = self.client.get_currencies()
                if not isinstance(response, list):
                    raise Exception("Unexpected response format")

                results = []
                for item in response:
                    results.append(SimpleNamespace(
                        symbol=item.get("currency", "") + "_usdt",  # 👈 Append _USDT here
                        quantityAccuracy=0,
                        priceAccuracy=item.get("maxPrecision", 8),  # Assuming same as quantity
                        minTranQua=0.0  # Not provided, using default
                    ))
                return results
            except Exception as e:
                print(f"[XT BasicDataMan] Error: {e}")
                print("Retrying after 15 seconds...")
                time.sleep(15)




    def getRatio(self, **d):
        pass

    def getWithdrawConf(self, **d):
        pass

    def getTimestamp(self):
        pass
