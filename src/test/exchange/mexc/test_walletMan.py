import pytest
import src.exchange.gateio.GateMarketMan as GateMarketMan
import src.exchange.gateio.github.gate_api.configuration as configuration
import src.exchange.gateio.github.gate_api.api_client as api_client
from datetime import datetime
import time
@pytest.mark.skip
def test_getMyPastTrades():
    configMan=configuration.Configuration(   key='cbf45c70a41d315d24e71e525db7a686',
        secret='4e068f14b767a90124b50162d1e65f3c85a26ed9afd794f067ebfefcf4b9dacc',
    )
    walletMan= GateMarketMan.GateMarketMan(api_client=api_client.ApiClient(configuration=configMan))
    #walletMan=spot_api.SpotApi()
    now=int(str(time.time()).split('.')[0])
    time.sleep(15)
    print(walletMan.my_trades(_from=now))
