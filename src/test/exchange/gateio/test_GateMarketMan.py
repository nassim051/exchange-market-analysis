import pytest, os, sys
import time
from datetime import datetime
"""path=os.path.join(os.path.dirname( __file__),'../../..')
sys.path.insert(0,path)
import exchange.gateio.GateMarketMan as gmm
sys.path.pop(0)
"""
import src.exchange.gateio.GateMarketMan as GateMarketMan
@pytest.mark.skip
def test_get_depth_without_errors():
    gate_market_man = GateMarketMan.GateMarketMan()
    result=gate_market_man.getDepth(symbol="BTC_USDT")
    print(result)
@pytest.mark.skip   
def test_get_trades_without_errors():
    gate_market_man = GateMarketMan.GateMarketMan()

    while True:
        timeNow=datetime.now()
        timeNow = str( timeNow.timestamp()  ).split( "." )[ 0 ]
        print(timeNow)
        time.sleep(10)
        result=gate_market_man.getTrades(symbol="BTC_USDT",size=6,time=timeNow)
        print(result)
        print(timeNow)
        print(len(result))
        timeNow=datetime.now()
        timeNow = str( timeNow.timestamp()  ).split( "." )[ 0 ]
        print(timeNow)
        return
    timeNow=datetime.now()
    timeNow = str( timeNow.timestamp()  ).split( "." )[ 0 ]
    result=gate_market_man.getTrades(symbol="BTC_USDT",size=6,time=1693703829)
    print(result[0].time)
#@pytest.mark.skip       
def test_kline():
    gate_market_man = GateMarketMan.GateMarketMan()
    result=gate_market_man.getKline(size=2,symbol="BTC_USDT",time=1712441738,type='hour1')
    print(result)