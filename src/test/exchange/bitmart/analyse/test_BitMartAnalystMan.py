import pytest
import src.exchange.bitmart.Analyse.BitMartAnalystMan as BitMartAnalystMan

bitmartAnalystMan = BitMartAnalystMan.BitMartAnalystMan(nbProcess=2)

@pytest.mark.skip
def test_updatePairs():
    bitmartAnalystMan.updatePairs()

@pytest.mark.skip
def test_findTokenWithGap():
    bitmartAnalystMan.findTokenWithGap()

@pytest.mark.skip
def test_countVolume():
    bitmartAnalystMan.countVolume(nbOfFetch=10, timeUnity=60, addOnDb=True)

@pytest.mark.skip
def test_deleteFutures():
    pairs = ['ETH_USDT', 'BTC_USDT', 'ETH3S_USDT', 'BTC5L_USDT']
    result = bitmartAnalystMan.deleteFutures(pairs)
    print("Filtered pairs:", result)

@pytest.mark.skip
def test_no_transactions():
    transactions = []
    gap = 0.01
    result = bitmartAnalystMan.countTransactionsWithGap(transactions, gap, 5.3, 5.3)
    assert result == (5.3, 5.3)

@pytest.mark.skip
def test_single_transaction():
    transactions = [{'amount': 55, 'price': 5.55}]
    gap = 0.01
    result = bitmartAnalystMan.countTransactionsWithGap(transactions, gap, 0, 0)
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
    nb, vol = bitmartAnalystMan.countTransactionsWithGap(transactions, gap, 0, 0)
    assert abs(vol - 11.80945) <= 0.001
    assert nb == 2
