import pytest
import time
from datetime import datetime
import src.exchange.mexc.MexcMarketMan as MexcMarketMan
from src.exchange.mexc.mexc_api_sdk.mexc_sdk.src.mexc_sdk import Spot
import src.db.DbManager as DbManager
@pytest.mark.skip
def test_get_depth_without_errors():

    response=MexcMarketMan.MexcMarketMan().getDepth(symbol='BTCUSDT')
    print(response)
       
    
@pytest.mark.skip
def test_get_trades_without_errors():
    timenow=int(datetime.now().timestamp()*1000)    
    time.sleep(30)
    print(MexcMarketMan.MexcMarketMan().getTrades(symbol='BTCUSDT',time=timenow))
@pytest.mark.skip
def test_getKline():
    mexcMarketMan=MexcMarketMan.MexcMarketMan()
    
#    result=Spot().klines(symbol="AESUSDT",interval="60m",options={"startTime":1712365399003,"limit":2000})

    prices=mexcMarketMan.getKline(size=2,symbol="BTCUSDT",time=1712441738000,type='hour1')
    print(prices[len(prices)-1])