# src/test/exchange/xt/test_XtBasicDataMan.py

import pytest
from types import SimpleNamespace
from src.exchange.Xt.XtBasicDataMan import XtBasicDataMan
@pytest.mark.skip
def test_get_accuracy_info():
    data_man = XtBasicDataMan()
    result = data_man.getAccuracyInfo()

    assert isinstance(result, list), "Result should be a list"
    assert len(result) > 0, "Result list should not be empty"
    assert isinstance(result[0], SimpleNamespace), "Each item should be a SimpleNamespace"

    # Print a sample for manual verification
    print("\nSample symbol data:")
    print(f"Symbol: {result[0].symbol}")
    print(f"Quantity Accuracy: {result[0].quantityAccuracy}")
    print(f"Price Accuracy: {result[0].priceAccuracy}")
    print(f"Min Transaction Quantity: {result[0].minTranQua}")
