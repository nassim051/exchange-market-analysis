import os
import sys
import time
from datetime import datetime, timedelta
import src.interface.TA.TaMan as taMan
from src.exchange.gateio.github.gate_api import ApiClient, Configuration
import src.exchange.gateio.github.gate_api.api.spot_api as SpotApi
import src.db.DbManager as DbManager
import src.exchange.gateio.Constants as credential
class OrderBookTrader:
    def __init__(self,symbol,buyAmount=0,sellAmount=0,interval="4h",limit=20, sleepTime=15, durtationMinutes=1440):
        self.symbol=symbol
        self.initial_buy_amount=self.buy_amount
        self.buyAmount=buyAmount
        self.sellAmount=self.sellAmount
        self.sleepTime=sleepTime
        self.durtationMinutes=durtationMinutes
        self.priceAccuracy=self.get_price_accuracy()
        self.buyJournal=[]
        self.averageBuy=0
        self.nonPendingBuy=False
        self.nonPendingSell=False
        self.buy_order_id=0
        self.sell_order_id=0
        self.order_book={}
        config = Configuration(key=credential.key, secret=credential.secret)
        self.spot_api = SpotApi.SpotApi(ApiClient(config))   
        self.dbManager= DbManager.DbManager()    
        self.interval=interval
        self.limit=limit
    def main(self):
        end_time = datetime.now() + timedelta(minutes=self.durtationMinutes)

        while datetime.now() < end_time:
            self.order_book=self.fetch_order_book()
            if self.buyAmount > 0:
                if self.is_order_pending(self.buy_order_id):
                    order_info=self.get_order_info(self.buy_order_id)
                    if self.order_executed(order_info, self.symbol, self.buyAmount):
                        executed_amount = self.get_executed_amount(order_info, self.symbol)
                        executed_price=self.get_executed_price(order_info,self.symbol)
                        fee=self.get_fee(order_info)

                        self.add_from_buy_journal(executed_price,executed_amount,fee)
                        self.sell_amount += executed_amount -fee
                        self.buyAmount -= executed_amount*executed_price
                        if self.buyAmount==0:
                            self.buy_order_id=0
                        else:
                            self.cancel_order(self.symbol, self.buy_order_id)
                            self.buy_order_id, buy_order_book = self.initialize_order("buy", self.buyAmount)
                        self.nonPendingSell=True
                    elif self.nonPendingBuy!=0 or self.order_book_has_changed(self.order_book, buy_order_book, 'buy') or self.order_executed(self.buy_order_id, self.symbol, self.buyAmount) :
                        self.cancel_order(self.symbol, self.buy_order_id)
                        self.buy_order_id, buy_order_book = self.initialize_order('buy', self.buyAmount)
                        self.nonPendingBuy=False
                else:
                    self.buy_order_id, buy_order_book = self.initialize_order("buy", self.buyAmount)
                    self.nonPendingBuy=False
 
            if self.sellAmount>0:
                if self.is_order_pending(self.sell_amount):
                    order_info=self.get_order_info(self.sell_order_id)
                    if self.sell_order_id: 
                        if self.order_executed(order_info, self.symbol, self.sell_amount):
                            executed_amount = self.get_executed_amount(order_info, self.symbol)
                            executed_price=self.get_executed_price(order_info,self.symbol)
                            fee=self.get_fee(order_info)
                            self.buyAmount += executed_amount*executed_price-fee
                            self.remove_from_buy_journal(executed_price,executed_amount)
                            self.sell_amount -= executed_amount
                            if self.sell_amount==0:
                                self.sell_order_id=0
                            else:
                                self.cancel_order(self.symbol, self.sell_order_id)
                                self.sell_order_idd,sell_order_book = self.initialize_order("sell", self.buyAmount)
                            self.nonPendingBuy=True
                            
                        elif self.nonPendingSell!=0 or self.order_book_has_changed(self.order_book, sell_order_book, 'sell') or self.order_executed(self.sell_order_id, self.symbol, self.sell_amount) :
                            self.cancel_order(self.symbol, self.sell_order_id)
                            self.sell_order_id, sell_order_book = self.initialize_order('sell', self.sell_amount)
                            self.nonPendingSell=False

                    else:
                        self.sell_order_id, sell_order_book = self.initialize_order("sell", self.sellAmount)
                        self.nonPendingSell=False
            time.sleep(self.sleepTime)


    def get_price_accuracy(self):
        currency_pair_details = self.spot_api.get_currency_pair(self.symbol)
    
        return 10**(-1*currency_pair_details.precision)

    def calculate_max_buy_price(self):
        prices = self.spot_api.list_candlesticks(currency_pair=self.symbol, interval=self.interval, limit=self.limit)
        return taMan.TaMan(prices).calculate_bollinger_bands()['lower_band']
    def calculate_min_sell_price(self):
        prices = self.spot_api.list_candlesticks(currency_pair=self.symbol, interval=self.interval, limit=self.limit)
        return taMan.TaMan().calculate_bollinger_bands(prices)['upper_band']
   
 

    def find_target_price(self,order_book, type, limit_price, chase_amount):
        if type == 'buy':
            for bid in order_book.bids:
                if bid[1] >= chase_amount and bid[0] < limit_price:
                    return bid[0] + self.priceAccuracy  # Just above the target
        elif type == 'sell':
            bought_price=self.get_purchased_price()
            for ask in order_book.asks:
                if ask[1] >= chase_amount and ask[0] > limit_price and ask[0]>bought_price*1.01:
                    return ask[0] - self.priceAccuracy  # Just below the target
        return None

    def execute_order(self, side, price, amount):
        while True:
            try:
                order = self.spot_api.create_order(
                    currency_pair=self.symbol,
                    side=side,
                    type='limit',  
                    price=str(price),
                    amount=str(amount)
                )
                print(f"Order executed: {side} {amount} at {price}")
                return order.id
            except Exception as e:
                print(f"Failed to execute order: {e} l'll retry after 15 seconds")
                time.sleep(15)

    def update_order_book(self,order_book, type, index, price, amount):
        if type == 'buy':
            if order_book.bids[index][0] == price:
                order_book.bids[index][1] += amount
            else:
                order_book.bids.insert(index, [price, amount])
        elif type == 'sell':
            if order_book.asks[index][0] == price:
                order_book.asks[index][1] += amount
            else:
                order_book.asks.insert(index, [price, amount])
        return order_book

    def order_book_has_changed(self,order_info, ob1, ob2, type):
        if type == 'buy':
            for i in range(min(len(ob1.bids), len(ob2.bids))):
                if ob2.bids[i][0] < order_info['data'][0]['price'] * 0.95:
                    break
                if ob1.bids[i][0] != ob2.bids[i][0]:
                    return True
            return False
        elif type == 'sell':
            for i in range(min(len(ob1.asks), len(ob2.asks))):
                if ob2.asks[i][0] > order_info['data'][0]['price'] * 1.05:
                    break
                if ob1.asks[i][0] != ob2.asks[i][0]:
                    return True
            return False
        return False


    def cancel_order(self, order_id):
        while True:
            try:
                self.spot_api.cancel_order(order_id, self.symbol)
                print(f"Order {order_id} cancelled.")
                return
            except Exception as e:
                print(f"Failed to cancel order: {e}, l'll sleep for 15 seconds")
                time.sleep(15)

    def update_amounts(self,order_type, amount, buy_quant, sell_quant, deal_amount, executed_order):
        amount -= (deal_amount - executed_order)
        if order_type == 'buy':
            buy_quant -= (deal_amount - executed_order)
        else:
            sell_quant -= (deal_amount - executed_order)
        return amount, buy_quant, sell_quant

    def initialize_order(self,order_type, amount):
        if order_type=="buy":
            limit_price=self.calculate_max_buy_price()
        else:
            limit_price=self.calculate_min_sell_price()
        price = self.find_target_price(self.order_book, order_type, limit_price, amount)
        self.order_id = self.execute_order( order_type, price, amount)
        self.order_book = self.update_order_book(self.order_book, order_type, 0, price, amount)


    def order_executed(self, order_info, symbol, amount):
        return order_info.fill_price > 0
 
    def get_executed_amount(self,order_info, symbol):
        return self.fill_price/self.price
    def get_executed_price(self,order_info, symbol):
        return order_info.price
    def get_fee(self,order_info):
        return order_info.fee
    def add_from_buy_journal(self, price, amount,fee):
        price=price*amount/(amount-fee)
        self.buyJournal.append({'price': price, 'amount': amount-fee})
    def remove_from_buy_journal(self, price, amount):
        self.buyJournal[0]['amount']-=amount

    def get_purchased_price(self):
        """
        Calculate the average purchase price for the last self.sellAmount 
        from the buy journal. Start from the most recent entries and move 
        backward to accumulate the needed amount.

        Returns:
            float: The average purchase price weighted by amounts.
        """
        total_usdt = 0
        total_amount=0
        for entry in self.buyJournal:

            total_usdt += entry['amount'] * entry['price']
            total_amount+=entry['amount']
        return total_usdt / total_amount

    def is_order_pending(self,order_id):
        return order_id!=0

    
    def get_order_info(self, order_id):
        while True:
            try:
                order = self.spot_api.get_order(order_id, self.symbol)
                return {
                    'id': order.id,
                    'status': order.status,
                    'filled_amount': float(order.filled_total),
                    'price': float(order.price)
                }
            except Exception as e:
                print(f"Failed to fetch order info: {e} l'll retry after 15 seconds")
                time.sleep(15)
    def fetch_order_book(self):
        while True:
            try:
                order_book = self.spot_api.list_order_book(self.symbol, limit=10)
                return {
                    'bids': [(float(b[0]), float(b[1])) for b in order_book.bids],
                    'asks': [(float(a[0]), float(a[1])) for a in order_book.asks]
                }
            except Exception as e:
                print(f"Failed to fetch order book: {e}, l'll sleep for 15 seconds")
                time.sleep(15)
    def get_price(self, symbol):
        while True:
            try:
                tickers = self.spot_api.list_tickers(currency_pair=symbol)
                if tickers and len(tickers) > 0:
                    return float(tickers[0].last)
                else:
                    print(f"No ticker data returned for {symbol}, retrying in 15 seconds...")
                    time.sleep(15)
            except Exception as e:
                print(f"Failed to fetch market price for {symbol}: {e}, I'll sleep for 15 seconds")
                time.sleep(15)

    def get_quote_amount(self,base_amount):
        return 1