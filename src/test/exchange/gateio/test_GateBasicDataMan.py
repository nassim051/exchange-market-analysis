import pytest, os, sys
import src.exchange.gateio.GateBasicDataMan as gbdm


def test_getAccuracyInfo():
    data_man = gbdm.GateBasicDataMan()  # Create an instance of GateBasicDataMan

    # Call the method, and if no exception is raised, the test passes
    response=data_man.getAccuracyInfo()
    print(response)
