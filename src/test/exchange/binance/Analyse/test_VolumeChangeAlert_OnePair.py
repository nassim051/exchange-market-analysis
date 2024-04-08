import pytest
# test_volume_change_alert.py

from src.exchange.binance.Analyse.VolumeChangeAlert_OnePair import VolumeChangeAlert_OnePair
from datetime import datetime, timedelta
@pytest.mark.skip
def test_run():
    # Create an instance of VolumeChangeAlert_OnePairs
    alert = VolumeChangeAlert_OnePair(interval=20000)

    # Call the `run` method with a specified number of hours
    nbHours = 24  # Example: Running for the past 24 hours
    alert.run(nbHours,symbol='ETHUSDT')
    alert.run(nbHours,symbol='BTCUSDT')

    # Add assertions if needed to check the behavior or output of the `run` method
