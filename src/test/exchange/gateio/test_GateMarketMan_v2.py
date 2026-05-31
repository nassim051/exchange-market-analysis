import pytest
import time
from datetime import datetime, timezone

# ⚠️ Adapte l'import au bon chemin vers ta classe GateIoMarketManV2
from src.exchange.gateio.GateMarketManV2 import GateIoMarketManV2


@pytest.mark.skip
def test_get_depth_without_errors():
    # conservé pour compatibilité avec ancien MarketMan
    pass


@pytest.mark.skip
def test_get_trades_without_errors():
    # conservé pour compatibilité avec ancien MarketMan
    pass


# ✅ Nouveau test de la méthode get_full_ohlcv_dataframe
#@pytest.mark.skip
def test_get_full_ohlcv_dataframe():
    client = GateIoMarketManV2()
    # Start date: September 1st, 2024 at 00:00 UTC
    start = datetime(2024, 9, 1, 0, 0, tzinfo=timezone.utc)
    # End date: April 1st, 2025 at 00:00 UTC
    end = datetime(2025, 4, 1, 0, 0, tzinfo=timezone.utc)

    df = client.get_full_ohlcv_dataframe(
        currency_pair="BTC_USDT",
        interval="4h",
        start=start,
        end=end
    )

    print(df.head())   # Show first few rows
    print(df.tail())   # Show last few rows
    print(f"Row count: {len(df)}")

    # Basic checks to make sure the data is valid
    assert not df.empty, "Returned DataFrame is empty"
    assert str(df.index.tz) == "UTC"
    assert all(col in df.columns for col in ["open", "high", "low", "close", "volume"]), "Missing expected columns"
    assert df.index.is_monotonic_increasing, "Timestamps are not sorted"