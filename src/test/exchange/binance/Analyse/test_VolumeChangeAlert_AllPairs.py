import pytest
# test_volume_change_alert.py

from src.exchange.binance.Analyse.VolumeChangeAlert_AllPairs import VolumeChangeAlert_AllPairs
from datetime import datetime, timedelta

def test_run():
    # Create an instance of VolumeChangeAlert_AllPairs
    alert = VolumeChangeAlert_AllPairs(interval=20000)

    # Call the `run` method with a specified number of hours
    nbHours = 24  # Example: Running for the past 24 hours
    alert.run(nbHours)

    # Add assertions if needed to check the behavior or output of the `run` method
