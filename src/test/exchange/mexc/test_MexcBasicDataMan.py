import pytest
import src.exchange.mexc.MexcBasicDataMan as MexcBasicDataMan

def test_getAccuracyInfo():
    print(len(MexcBasicDataMan.MexcBasicDataMan().getAccuracyInfo()))

    