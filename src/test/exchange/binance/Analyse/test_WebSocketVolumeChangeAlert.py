import pytest

# test_volume_change_alert.py

from src.exchange.binance.Analyse.WebSocketVolumeChangeAlert import WebSocketVolumeChangeAlert
from datetime import datetime, timedelta

def test_run():
    # Create an instance of WebSocketVolumeChangeAlerts
    alert = WebSocketVolumeChangeAlert(interval=20000,symbol='BTCUSDT')

    # Call the `run` method with a specified number of hours
    nbHours = 24  # Example: Running for the past 24 hours
    alert.run()

    # Add assertions if needed to check the behavior or output of the `run` method
