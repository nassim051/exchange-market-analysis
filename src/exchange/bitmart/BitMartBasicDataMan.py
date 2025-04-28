from types import SimpleNamespace
import src.interface.IBasicDataMan as ibdm
from bitmart.api_spot import APISpot as SpotClient
from bitmart.lib import cloud_exceptions
import time

class BitMartBasicDataMan(ibdm.IBasicDataMan):
    def __init__(self):
        self.client = SpotClient()

    def getAccuracyInfo(self):
        while True:
            try:
                response = self.client.get_symbol_detail()
                symbols = response[0]['data']['symbols']
                break
            except Exception as e:
                print(f"[BitMart] Error fetching symbol data: {e}")
                time.sleep(10)
        result = []

        for symbol in symbols:
            result.append(
                SimpleNamespace(
                    symbol=symbol['symbol'],
                    quantityAccuracy=0,  # BitMart does not expose this directly
                    priceAccuracy=int(symbol['price_max_precision']),
                    minTranQua=float(symbol['base_min_size'])
                )
            )
        return result

    def getcurrencyPairs(self):
        return [s.symbol for s in self.getAccuracyInfo()]

    def getRatio(self, **d):
        pass

    def getWithdrawConf(self, **d):
        pass

    def getTimestamp(self):
        return int(time.time())
