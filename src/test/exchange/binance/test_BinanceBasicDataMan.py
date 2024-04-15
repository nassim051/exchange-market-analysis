import pytest
import time
from datetime import datetime
from src.exchange.binance.binance_git.binance.spot import Spot
import src.exchange.binance.BinanceBasicDataMan as BinanceBasicDataMan
#@pytest.mark.skip
def test_getAccuracyInfo():
    binanceMarketMan=BinanceBasicDataMan.BinanceBasicDataMan()
    timenow=int(datetime.now().timestamp()*1000)    
    spot=Spot()
    try:
        vol=binanceMarketMan.getAccuracyInfo()

    except Exception as e:
        print(f"Following exception occured: {e.status_code}")
        return
    print(vol['symbols'])