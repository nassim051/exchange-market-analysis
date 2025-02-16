from datetime import datetime, timedelta
import src.interface.Trade.OrderBookTrader as OrderBookTrader
import pytest, os, sys
from src.exchange.gateio.github.gate_api import ApiClient, Configuration
import src.exchange.gateio.github.gate_api.api.spot_api as SpotApi
import src.exchange.gateio.Constants as credential
import time
import src.interface.TA.TaMan as taMan




config = Configuration(key=credential.key, secret=credential.secret)
spot = SpotApi.SpotApi(ApiClient(config))   


@pytest.mark.skip(reason="Skipping the test for Gate IO API")
def test_api_key_api():
    config = Configuration(key=credential.key, secret=credential.secret)
    print(config)

@pytest.mark.skip(reason="Skipping the test for Gate IO API")
def test_price_accuracy():
    currency_pair_details =  spot.get_currency_pair('DMC_USDT')
    print(f"precision: {currency_pair_details.precision}")    
@pytest.mark.skip(reason="Skipping the test for Gate IO API")
def test_order_book():
    order_book = spot.list_order_book('DMC_USDT', limit=10)

    order_book_updated={
                    'bids': [(float(b[0]), float(b[1])) for b in order_book.bids],
                    'asks': [(float(a[0]), float(a[1])) for a in order_book.asks]
                }
    print(order_book_updated)
@pytest.mark.skip(reason="Skipping the test for Gate IO API")
def test_time():
    end_time=datetime.now() + timedelta(minutes=1)
    print(f"current time: {datetime.now()}")
    print(f"endTime: {end_time}")
    while(datetime.now()<end_time):
        print(f"current time: {datetime.now()}")
        print(f"endTime: {end_time}")
        time.sleep(15)




@pytest.mark.skip(reason="Skipping the test for Gate IO API")
def test_get_order_info():
    order = spot.get_order(775824841017, 'DMC_USDT')
    print(order)

@pytest.mark.skip(reason="Skipping the test for Gate IO API")
def test_initialize_order():
    order=spot.create_order(order={
          "currency_pair":"GT_USDT",
          "side":"sell",
          "type":"limit",
          "price":"21.394",
          "amount":"0.16"})
    print(f"order: {order}")
"""
response of create order endpoint buy:
{'account': 'spot',
 'amend_text': '-',
 'amount': '400',
 'auto_borrow': None,
 'auto_repay': None,
 'avg_deal_price': None,
 'create_time': '1739124909',
 'create_time_ms': 1739124909893,
 'currency_pair': 'DMC_USDT',
 'fee': '0',
 'fee_currency': 'DMC',
 'fill_price': '0',
 'filled_total': '0',
 'finish_as': 'open',
 'gt_discount': False,
 'gt_fee': '0',
 'gt_maker_fee': '0',
 'gt_taker_fee': '0',
 'iceberg': '0',
 'id': '791774189174',
 'left': '400',
 'point_fee': '0',
 'price': '0.019',
 'rebated_fee': '0',
 'rebated_fee_currency': 'USDT',
 'side': 'buy',
 'status': 'open',
 'stp_act': None,
 'stp_id': None,
 'text': 'apiv4',
 'time_in_force': 'gtc',
 'type': 'limit',
 'update_time': '1739124909',
 'update_time_ms': 1739124909893}



 exemple for sell:
 ,
 'amend_text': '-',
 'amount': '0.16',
 'auto_borrow': None,
 'auto_repay': None,
 'avg_deal_price': '21.434',
 'create_time': '1739147522',
 'create_time_ms': 1739147522747,
 'currency_pair': 'GT_USDT',
 'fee': '0.0033951456',
 'fee_currency': 'USDT',
 'fill_price': '3.42944',
 'filled_total': '3.42944',
 'finish_as': 'filled',
 'gt_discount': False,
 'gt_fee': '0',
 'gt_maker_fee': '0',
 'gt_taker_fee': '0',
 'iceberg': '0',
 'id': '791912019502',
 'left': '0',
 'point_fee': '0',
 'price': '21.394',
 'rebated_fee': '0',
 'rebated_fee_currency': 'GT',
 'side': 'sell',
 'status': 'closed',
 'stp_act': None,
 'stp_id': None,
 'text': 'apiv4',
 'time_in_force': 'gtc',
 'type': 'limit',
 'update_time': '1739147522',
 'update_time_ms': 1739147522747}
"""
@pytest.mark.skip(reason="Skipping the test for Gate IO API")
def test_get_price():
        prices = spot.list_candlesticks(currency_pair='DMC_USDT', interval='4h', limit=20)
        print(f"bollinger: {taMan.TaMan(prices).calculate_bollinger_bands()['lower_band']}")

@pytest.mark.skip(reason="Skipping the test for Gate IO API")
def test_limite_price_buy():
    chase_amount=10
    currency_pair_details = spot.get_currency_pair('DMC_USDT')   
    priceAccuracy= 10**(-1*currency_pair_details.precision)
    print(f"price accuracy:{priceAccuracy}")
    order_book = spot.list_order_book('DMC_USDT', limit=100)
    prices = spot.list_candlesticks(currency_pair='DMC_USDT', interval='4h', limit=20)
    limit_price=taMan.TaMan(prices).calculate_bollinger_bands()['lower_band']
    print(f"imit price:{limit_price}")
    buyprice=-1
    for bid in order_book.bids:
        bid[0]=float(bid[0])
        bid[1]=float(bid[1])
        if bid[1] >= chase_amount and bid[0] < limit_price:
            print(f"l'll place an order in {bid[0]}+{priceAccuracy}")
            buyprice= bid[0] + priceAccuracy  # Just above the target
            break
    if buyprice==-1:
        print("didn't find an optimal price, maybe you should go deeper in order book or have a look at your chase amount")
    else:
        print(f"buy price:{buyprice}")


def test_limite_price_sell():
    chase_amount=5000
    currency_pair_details = spot.get_currency_pair('DMC_USDT')   
    priceAccuracy= 10**(-1*currency_pair_details.precision)
    print(f"price accuracy:{priceAccuracy}")
    order_book = spot.list_order_book('DMC_USDT', limit=100)   
    prices = spot.list_candlesticks(currency_pair='DMC_USDT', interval='4h', limit=20)
    limit_pricer=taMan.TaMan(prices)
    print(f"moving average: {limit_pricer.calculate_bollinger_bands()['middle_band']} upper band: {limit_pricer.calculate_bollinger_bands()['upper_band']}")
    limit_price=(limit_pricer.calculate_bollinger_bands()['middle_band']+limit_pricer.calculate_bollinger_bands()['upper_band'])/2
    print(f"limit price:{limit_price}")
    sellPrice=-1
    for ask in order_book.asks:
        ask[0]=float(ask[0])
        ask[1]=float(ask[1])
    bought_price=0.01965

    for ask in order_book.asks:
            if ask[1] >= chase_amount and ask[0] > limit_price and ask[0]>bought_price*1.01:
                print(f"l'll place an order in {ask[0]}-{priceAccuracy}")
                sellPrice= ask[0] - priceAccuracy
                break
    if sellPrice==-1:
        print("didn't find an optimal price, maybe you should go deeper in order book or have a look at your chase amount")
    else:
        print(f"buy price:{sellPrice}")

"""
bought_price=self.get_purchased_price()
            for ask in order_book.asks:
                if ask[1] >= chase_amount and ask[0] > limit_price and ask[0]>bought_price*1.01:
                    return ask[0] - self.priceAccuracy  # Just below the target
"""