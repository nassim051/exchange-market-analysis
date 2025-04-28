import pytest
from src.exchange.bitmart.BitMartBasicDataMan import BitMartBasicDataMan

def test_getAccuracyInfo():
    data_man = BitMartBasicDataMan()
    result = data_man.getAccuracyInfo()
    print(result)