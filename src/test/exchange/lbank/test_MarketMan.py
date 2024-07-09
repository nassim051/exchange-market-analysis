import pytest, os, sys
import src.exchange.lbank.MarketMan as MarketMan
import src.exchange.lbank.OrdersMan as OrdersMan
import src.exchange.lbank.new_v2_inter.OrderMan as OrderMan
import src.exchange.lbank.new_v2_inter.WalletMan as WalletMan
import src.exchange.lbank.new_v2_inter.MarketMan as MarketManV2
#@pytest.mark.skip
def test_getDepth():
    data_man = MarketMan.MarketMan()
    # Call the method, and if no exception is raised, the test passes
    response=data_man.getDepth(symbol='btc_usdt',size=10,merge=0)
    print(response)
@pytest.mark.skip
def test_getTrades():
    response=MarketMan.MarketMan().getTrades(symbol='btc_usdt',size='600')
    print(response)

@pytest.mark.skip
def test_listOrders():
    orderMan=OrderMan.OrderMan().getTransaction_history(symbol='btc_usdt',current_page=1,page_length=2)
    ordersMan=OrdersMan.Orders().getHistTran(symbol='btc_usdt',current_page=1,page_length=2)
    print(f"V2: {orderMan}")
    print(f"normal: {ordersMan}")



@pytest.mark.skip
def test_getTicker():
    response=MarketMan.MarketMan().getTicker(symbol='sos_usdt')
    print(response)


def test_getKline():
    prices=MarketMan.MarketMan().getKline(symbol='btc_usdt',size=100,type="minute1",time=1712433441)
    print(prices[len(prices)-1])