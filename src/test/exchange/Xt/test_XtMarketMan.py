from datetime import datetime, timedelta
import pytest
from src.exchange.Xt.XtMarketMan import XtMarketMan
from src.exchange.Xt.XtBasicDataMan import XtBasicDataMan

import time  # make sure you import time module
from datetime import datetime, timedelta

@pytest.mark.skip
def test_get_depth():
    market_man = XtMarketMan()
    result = market_man.getDepth(symbol="btc_usdt")
    assert result != -1
    assert hasattr(result, 'asks') and hasattr(result, 'bids')
    print("\n[XT] Order Book Asks Sample:", result.asks[:2])



@pytest.mark.skip
def test_get_trades_with_time():
    market_man = XtMarketMan()
    # Get timestamp for 30 seconds ago
    thirty_seconds_ago = int((datetime.now() - timedelta(hours=4)).timestamp() * 1000)
    print(f"from:{thirty_seconds_ago}")
    # Fetch trades since that timestamp
    result = market_man.getTrades(symbol="btc_usdt", size=1000, time=thirty_seconds_ago)
    print("\n[XT] Trades Sample:", result)


#@pytest.mark.skip
def test_get_kline():
    market_man = XtMarketMan()
    
    start_time_ms = int((datetime.now() - timedelta(hours=24)).timestamp() * 1000)
    now_ms = int(time.time() * 1000)

    klines = market_man.getKline(
        symbol="BTC_USDT",
        type="1h",

        time=start_time_ms
    )

    print(klines)
    print(int(klines[len(klines)-1].time)+int(timedelta(hours=1).total_seconds())*1000<now_ms and len(klines)!=0)
    print(klines[len(klines)-1].time)


 
