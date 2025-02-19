import pytest
import src.exchange.mexc.MexcBasicDataMan as MexcBasicDataMan


#@pytest.mark.skip
def test_getAccuracyInfo():
    print(len(MexcBasicDataMan.MexcBasicDataMan().getAccuracyInfo()))

    