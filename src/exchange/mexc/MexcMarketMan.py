import requests
import time
import json
from datetime import datetime
import src.exchange.mexc.models.Kline as Kline
import src.exchange.mexc.models.OrderBook as modelOrderBook
import src.exchange.mexc.models.Transaction as modelTransaction
import src.interface.IMarketMan as imm
from .api import make_request  
 
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
        pass

 

    def getTrades(self, **d):
        start_time = int(d['time'])
        end_time = int(datetime.now().timestamp() * 1000)
        params = {"symbol": d['symbol'], "startTime": start_time, "endTime": end_time}
        
        while True:
            response = make_request("aggTrades", params)
            if response == "TIMEOUT":
                print("Request timed out. Sleeping for 1 minute...")
                time.sleep(60)
            elif isinstance(response, str):
                print(f"An exception occurred: {response}")
            elif response is not None:
                return modelTransaction.editJsonResponse(response)
            
            print("I'm going to sleep for 15 seconds")
            time.sleep(15)

    def getKline(self, **d):
        start_time = int(d['time'])
        limit = int(d['size'])
        interval = STANDARD_TIME_TO_MEXC_TIME_MAP[d['type']]
        params = {"symbol": d['symbol'], "interval": interval, "startTime": start_time, "limit": limit}
        
        while True:
            response = make_request("klines", params)
            if response == "TIMEOUT":
                print("Request timed out. Sleeping for 1 minute...")
                time.sleep(60)
            elif isinstance(response, str):
                print(f"An exception occurred: {response}")
            elif response is not None:
                return Kline.editJsonResponse(response)
            
            print("I'm going to sleep for 15 seconds")
            time.sleep(15)

    def getDepth(self, **d):
        params = {"symbol": d['symbol'], "limit": 10}
        
        while True:
            response = make_request("depth", params)
            if response == "TIMEOUT":
                print("Request timed out. Sleeping for 1 minute...")
                time.sleep(60)
            elif isinstance(response, str):
                if "Invalid symbol." in response:
                    print(f"The order book is empty or unavailable for: {d['symbol']}")
                    return -1
                print(f"An exception occurred: {response}")
            elif response is not None:
                return modelOrderBook.editJsonResponse(response)
            
            print("I'm going to sleep for 15 seconds")
            time.sleep(15)
    
    def getTicker(self, **d):
        # Implement getTicker method for GateMarketMan
        pass
    
    def getIncrDepth(self, **d):
        # Implement getIncrDepth method for GateMarketMan
        pass
