import pytest
from src.exchange.bitmart.BitMartMarketMan import BitMartMarketMan
import time
from datetime import datetime

@pytest.mark.skip
def test_get_depth():
    market_man = BitMartMarketMan()
    result = market_man.getDepth(symbol="BTC_USDT")
    print(result)
@pytest.mark.skip
def test_get_trades():
    market_man = BitMartMarketMan()
    now = int(datetime.now().timestamp())
    result = market_man.getTrades(symbol="BTC_USDT", size=5, time=now - 60)
    assert isinstance(result, list)
    print(result)
#@pytest.mark.skip
def test_get_kline():
    market_man = BitMartMarketMan()
    now = int(time.time()) - 3600 * 24
    result = market_man.getKline(size=5, symbol="BTC_USDT", time=now, type="1h")
    assert isinstance(result, list)
    print(result)
