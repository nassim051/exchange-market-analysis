import os
import sys
import time
from datetime import datetime, timedelta
import src.interface.TA.TaMan as taMan
# Setup import paths
path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, path)
import AccountMan as ac
import new_v2_inter.MarketMan as nma
import MarketMan as marketMan
import OrdersMan as ordersMan
import models.Order_Book as mod
import db.Insert_Data as dbid
import db.Select_Data as dbsd
sys.path.pop(0)

class orderBookTrader:
    def __init__(self,symbol,buyAmount=0,sellAmount=0, sleepTime=15, durtationMinutes=1440):
        self.symbol=symbol
        self.buyAmount=buyAmount
        self.sellAmount=sellAmount
        self.sleepTime=sleepTime
        self.durtationMinutes=durtationMinutes
        
    def main(self):
        end_time = datetime.now() + timedelta(minutes=self.durtationMinutes)
        while datetime.now() < end_time:
            try:
                response = ac.AccountMan().getUserInfo()
                self.sell_amount = min(float(response['data']['free'][self.symbol.split('_')[0]]), self.sell_amount)
            except KeyError:
                print('Key error exception in data')
                time.sleep(5)
                continue

            if self.buy_amount > 0:
                if self.there_is_no_pending_order():
                    buy_order_id, buy_order_book = self.initialize_order(self.symbol, "buy", self.buy_amount)

                elif self.order_executed(buy_order_id, self.symbol, self.buy_amount):
                    self.update_buy_journal()
                    executed_amount = self.get_executed_amount(buy_order_id, self.symbol)
                    self.sell_amount += executed_amount 
                    self.buy_amount -= executed_amount
                if self.order_book_has_changed(mod.LoadOrderBook.fetchOrderBook(self.symbol), buy_order_book, 'buy') or self.order_executed(buy_order_id, self.symbol, self.buy_amount) :
                    self.cancel_order(self.symbol, buy_order_id)
                    buy_order_id, buy_order_book = self.initialize_order(self.symbol, 'buy', self.buy_amount)
            if self.sell_amount > 0:
                if self.there_is_no_pending_order():
                    sell_order_id, sell_order_book = self.initialize_order(self.symbol, "sell", self.sell_amount)
                if self.order_executed(sell_order_id, self.symbol, self.sell_amount):
                    executed_amount = self.get_executed_amount(sell_order_id, self.symbol)
                    self.buy_amount += executed_amount
                    self.sell_amount -= executed_amount
                if self.order_book_has_changed(mod.LoadOrderBook.fetchOrderBook(self.symbol), sell_order_book, 'sell') or self.order_executed(sell_order_id, self.symbol, self.sell_amount) :
                    self.cancel_order(self.symbol, sell_order_id)
                    sell_order_id, sell_order_book = self.initialize_order(self.symbol, 'sell', self.sell_amount)

            time.sleep(self.sleepTime)


    # Helper functions
    def get_price_accuracy(self,symbol):
        response = dbsd.selectFromDb('pair', 'priceAccuracy', condition="symbol", data=symbol)
        return response

    def calculate_max_buy_price(self):
        prices=marketMan.getPrice(self.symbol)
        return taMan.TaMan().bollingerBands(prices)[2]
    def calculate_min_sell_price(self):
        prices=marketMan.getPrice(self.symbol)
        return taMan.TaMan().bollingerBands(prices)[0]
   
    def calculate_chase_amount(self,order_book, type):
        return 1000  # Placeholder amount

    def find_target_price(self,order_book, type, limit_price, chase_amount):
        if type == 'buy':
            for bid in order_book.bids:
                if bid[1] >= chase_amount and bid[0] < limit_price:
                    return bid[0] + 0.01  # Just above the target
        elif type == 'sell':
            for ask in order_book.asks:
                if ask[1] >= chase_amount and ask[0] > limit_price:
                    return ask[0] - 0.01  # Just below the target
        return None

    def execute_order(self,symbol, type, price, amount):
        orderMan = orderMan.Orders()
        result = orderMan.createOrders(symbol=symbol, type=type, price=price, amount=amount, customer_id='')
        return result['data']['order_id']

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

    def cancel_order(self,symbol, order_id):
        orderMan = om.Orders()
        while True:
            response = orderMan.cancelOrders(symbol=symbol, order_id=order_id)
            if response['result']:
                break
            else:
                print("Failed to cancel the order, retrying...")
                time.sleep(5)

    def update_amounts(self,order_type, amount, buy_quant, sell_quant, deal_amount, executed_order):
        amount -= (deal_amount - executed_order)
        if order_type == 'buy':
            buy_quant -= (deal_amount - executed_order)
        else:
            sell_quant -= (deal_amount - executed_order)
        return amount, buy_quant, sell_quant

    def initialize_order(self,symbol, order_type, amount):
        if order_type=="buy":
            limit_price=self.calculate_max_buy_price()
        else:
            limit_price=self.calculate_min_sell_price()
        chase_amount = self.calculate_chase_amount(mod.LoadOrderBook.fetchOrderBook(symbol), order_type)
        price = self.find_target_price(mod.LoadOrderBook.fetchOrderBook(symbol), order_type, limit_price, chase_amount)
        order_id = self.execute_order(symbol, order_type, price, amount)
        order_book = self.update_order_book(mod.LoadOrderBook.fetchOrderBook(symbol), order_type, 0, price, amount)
        return order_id, order_book


    def order_executed(self, order_id, symbol, amount):
        orderMan = om.Orders()
        order_info = orderMan.getOrderInfo(symbol=symbol, order_id=order_id)
        return order_info['data'][0]['deal_amount'] < amount and order_info['data'][0]['deal_amount'] > 0
    def there_is_no_pending_order(self):
        return True
    def get_executed_amount(self,order_id, symbol):
        orderMan = om.Orders()
        order_info = orderMan.getOrderInfo(symbol=symbol, order_id=order_id)
        return order_info['data'][0]['deal_amount']

    def update_buy_journal(self):
        a=0
