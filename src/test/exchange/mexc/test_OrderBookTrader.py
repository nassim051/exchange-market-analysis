from src.exchange.mexc.mexc_api_sdk.mexc_sdk.src.mexc_sdk import Spot

api_key = 'mx0vglWk1i8aFNvZQq'
api_secret = '3d6243b85cd444b7b155f4eb7d1443bd'

client = Spot(api_key, api_secret)

# Fetch open orders for a symbol
def test_open_orders():
    # Fetch open orders for a symbol
    response = client.open_orders(symbol='CWAUSDT')
    print(f"response: {response}")

