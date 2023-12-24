import src.exchange.lbank.analyse.LBankAnalystMan as LBankAnalystMan
import pytest
import src.exchange.lbank.new_v2_inter.MarketMan as MarketMan
import src.exchange.lbank.MarketMan as MarketMan2

LBankAnalystMan=LBankAnalystMan.LBankAnalystMan()
@pytest.mark.skip
def test_updatePairs():
    LBankAnalystMan.updatePairs()
@pytest.mark.skip
def test_findTokenWithGap():
    LBankAnalystMan.findTokenWithGap()
@pytest.mark.skip
def test_countVolume():
    LBankAnalystMan.countVolume(10,60,True,symbol=("bal_usdt","ren_usdt","rpl_usdt","crv_usdt","efk_usdt","flm_usdt","meme_usdt","tvk_usdt","grt_usdt","pond_usdt","pce_usdt","1inch_usdt","sdt_usdt","lit_usdt","bnt_usdt","axs_usdt","elcash_usdt","fei_usdt","fine_usdt","tru_usdt","kabosu_usdt","babydoge_usdt","tlm_usdt","saitama_usdt","yoshi_usdt","xt_usdt","aca_usdt","crp_usdt","bio_usdt","magic_usdt","mr_usdt","sys_usdt","klee_usdt","bfic_usdt","jasmy_usdt","cult_usdt"))
   
@pytest.mark.skip
def test_deleteFutures():
    result=LBankAnalystMan.deleteFutures('ETH_USDT','ETH3S_USDT','BTC_USDT','R2L_USDT')
    print(result)
@pytest.mark.skip
def test_no_transactions():
    transactions = []
    gap = 0.01
    result = LBankAnalystMan.countTransactionsWithGap(transactions, gap,5.3,5.3)
    assert result == (5.3, 5.3)
@pytest.mark.skip
def test_single_transaction():
    transactions = [{'amount': 55, 'price': 5.55}]
    gap = 0.01
    result = LBankAnalystMan.countTransactionsWithGap(transactions, gap,0,0)
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
    nb, vol = LBankAnalystMan.countTransactionsWithGap(transactions, gap,0,0)
    assert abs(vol-11.80945) <=0.001
    assert nb==2
def test_getTransactionHistory():
    #print(MarketMan2.MarketMan().getTicker(symbol='bitcoin_usdt')['data'][0]['ticker']['latest'])
    LBankAnalystMan.getTransactionHistory(15)
