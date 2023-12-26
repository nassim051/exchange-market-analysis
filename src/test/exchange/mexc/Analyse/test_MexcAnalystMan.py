import src.exchange.mexc.Analyse.MexcAnalystMan as MexcAnalystMan
import pytest
from src.exchange.mexc.mexc_api_sdk.mexc_sdk.src.mexc_sdk import Spot


mexcAnalystMan=MexcAnalystMan.MexcAnalystMan()
@pytest.mark.skip
def test_updatePairs():
    mexcAnalystMan.updatePairs()
@pytest.mark.skip  
def test_findTokenWithGap():
    mexcAnalystMan.findTokenWithGap()
@pytest.mark.skip  
def test_countVolume():
    mexcAnalystMan.countVolume(10,60,True)
   
@pytest.mark.skip
def test_deleteFutures():
    result=mexcAnalystMan.deleteFutures('ETH_USDT','ETH3S_USDT','BTC_USDT','R2L_USDT')
    print(result)
@pytest.mark.skip
def test_no_transactions():
    transactions = []
    gap = 0.01
    result = mexcAnalystMan.countTransactionsWithGap(transactions, gap,5.3,5.3)
    assert result == (5.3, 5.3)
@pytest.mark.skip
def test_single_transaction():
    transactions = [{'amount': 55, 'price': 5.55}]
    gap = 0.01
    result = mexcAnalystMan.countTransactionsWithGap(transactions, gap,0,0)
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
    nb, vol = mexcAnalystMan.countTransactionsWithGap(transactions, gap,0,0)
    assert abs(vol-11.80945) <=0.001
    assert nb==2
#@pytest.mark.skip   
def  test_getTransactionHistory():
    Spot(api_key='mx0vglvIlls4RraSCH',api_secret='7521f7de355d4c54aa5b34d6d0e21822').historical_trades
    #print(Spot(api_key='mx0vglvIlls4RraSCH',api_secret='7521f7de355d4c54aa5b34d6d0e21822').account_info())
    #print(Spot(api_key='mx0vglvIlls4RraSCH',api_secret='7521f7de355d4c54aa5b34d6d0e21822').all_orders(symbol='HUAHUA'+'USDT',options={'startTime':1703105868000}))
    mexcAnalystMan.getTransactionHistory(15)
