import pytest
import time
from datetime import datetime
from src.exchange.binance.binance_git.binance.spot import Spot
import src.exchange.binance.BinanceMarketMan as BinanceMarketMan
#@pytest.mark.skip
def test_get_kline():
    binanceMarketMan=BinanceMarketMan.BinanceMarketMan()
    timenow=int(datetime.now().timestamp()*1000)    
    spot=Spot()
    try:
        vol=binanceMarketMan.getKline(size=2,symbol="BTCUSDT",time=1712441738000,type='hour1')

    except Exception as e:
        print(f"Following exception occured: {e.status_code}")
        return
    print(vol)