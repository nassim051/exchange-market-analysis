import src.exchange.gateio.Analyse.GateioAnalystMan as GateioAnalystMan
import pytest


gateioAnalystMan=GateioAnalystMan.GateioAnalystMan()

@pytest.mark.skip
def test_updatePairs():
    gateioAnalystMan.updatePairs()
#@pytest.mark.skip  
def test_findTokenWithGap():
    gateioAnalystMan.findTokenWithGap()
@pytest.mark.skip  
def test_countVolume():
    gateioAnalystMan.countVolume(10,60,True)
   
@pytest.mark.skip
def test_deleteFutures():
    result=gateioAnalystMan.deleteFutures('ETH_USDT','ETH3S_USDT','BTC_USDT','R2L_USDT')
    print(result)
@pytest.mark.skip
def test_no_transactions():
    transactions = []
    gap = 0.01
    result = gateioAnalystMan.countTransactionsWithGap(transactions, gap,5.3,5.3)
    assert result == (5.3, 5.3)
@pytest.mark.skip
def test_single_transaction():
    transactions = [{'amount': 55, 'price': 5.55}]
    gap = 0.01
    result = gateioAnalystMan.countTransactionsWithGap(transactions, gap,0,0)
    assert result == (0, 0)
@pytest.mark.skip   
def test_multiple_transactions():
    transactions = [
        {'amount': 55, 'price': 5.55},
        {'amount': 87, 'price': 6.0},
        {'amount': 42, 'price': 4.95},
        {'amount': 60, 'price': 4.97},
    ]
    gap = 0.01
    nb, vol = gateioAnalystMan.countTransactionsWithGap(transactions, gap,0,0)
    assert abs(vol-11.80945) <=0.001
    assert nb==2
def  test_getTransactionHistory():
    gateioAnalystMan.getTransactionHistory(15)
