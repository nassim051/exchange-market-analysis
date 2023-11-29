import pytest, os, sys
import src.exchange.lbank.MarketMan as MarketMan

import src.exchange.lbank.new_v2_inter.MarketMan as MarketManV2
def test_getDepth():
    data_man = MarketMan.MarketMan()
    # Call the method, and if no exception is raised, the test passes
    response=data_man.getDepth(symbol='btc_usdt',size=10,merge=0)
    print(response)
@pytest.mark.skip
def test_getTrades():
    response=MarketMan.MarketMan().getTrades(symbol='btc_usdt',size='600')
    print(response)