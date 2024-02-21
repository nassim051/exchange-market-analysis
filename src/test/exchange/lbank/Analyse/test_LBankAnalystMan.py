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
#@pytest.mark.skip
def test_countVolume():
    LBankAnalystMan.countVolume(10,60,True,symbol=("grv_usdt","gdcc_usdt","mshd_usdt","rndr_usdt","mob_usdt","imgnai_usdt","rdnt_usdt","mtvt_usdt","fis_usdt","ria_usdt","core_usdt","kava_usdt","ssv_usdt","lgc_usdt","wv_usdt","mudi_usdt","blur_usdt","ent_usdt","acs_usdt","tra_usdt","fra_usdt","gns_usdt","wen_usdt","infi_usdt","soc_usdt","zkf_usdt","camly_usdt","gme_usdt","2ped_usdt","pork_usdt","dmail_usdt","lzm_usdt","reel_usdt","sxio_usdt","jup_usdt","zeta_usdt","drm_usdt","nuts_usdt","dwars_usdt","pandora_usdt","pwc_usdt","coon_usdt","oas_usdt","bom_usdt","hpo_usdt","navx_usdt","dym_usdt","pbu_usdt"))
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
