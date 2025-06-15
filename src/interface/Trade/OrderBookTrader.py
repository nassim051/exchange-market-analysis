import os
import sys
import time
import random
from datetime import datetime, timedelta
import src.interface.TA.TaMan as taMan
from src.exchange.gateio.github.gate_api import ApiClient, Configuration
from src.exchange.gateio.GateMarketManV2 import GateIoMarketManV2
import src.db.DbManager as DbManager
import src.exchange.gateio.Constants as credential
from decimal import Decimal
class OrderBookTrader:
    def __init__(self,symbol,chase_amount,buyAmount=0,sellAmount=0,interval="4h",limit=20):
        self.symbol=symbol
        self.buyAmount=buyAmount
        self.chase_amount=chase_amount
        self.initial_buy_amount=self.buyAmount
        self.sellAmount=sellAmount
        self.buyJournal=[]
        self.averageBuy=0
        self.nonPendingBuy=False
        self.nonPendingSell=False
        self.buy_order_id=0
        self.sell_order_id=0
        self.order_book={}
        self.buy_order_book={}
        self.sell_order_book={}
        self.taMan= taMan.TaMan()
        self.spot_api = GateIoMarketManV2()

        self.priceAccuracy=self.get_price_accuracy()

        self.dbManager= DbManager.DbManager()    
        self.interval=interval
        self.limit=limit
    def main(self):
            self.order_book=self.fetch_order_book()
            if self.buyAmount > 0 and self.buyAmount*self.order_book.bids[0][0]>3:
                if self.is_order_pending(self.buy_order_id):
                    order_info=self.get_order(self.buy_order_id)
                    if self.order_executed(order_info):
                        executed_amount = self.get_executed_amount(order_info, self.symbol)
                        print(f"executed amount: {executed_amount}")
                        executed_price=self.get_executed_price(order_info,self.symbol)
                        print(f"executed price: {executed_price}")

                        fee=self.get_fee(order_info)

                        self.add_from_buy_journal(executed_price,executed_amount,fee)
                        print(f"buy journal : {self.buyJournal}")
                        self.sellAmount += executed_amount -fee
                        print(f"sell amount : {self.sellAmount}")
                        self.buyAmount -= executed_amount
                        print(f"buy amount : {self.buyAmount}")
                        if executed_amount >= 0.99999 * self.buyAmount: 
                            print("no buy order anymore")
                            self.buy_order_id=0
                            self.buyAmount=0
                        else:
                            self.cancel_order( self.buy_order_id,order_info)
                            self.buy_order_id=self.initialize_order("buy", self.buyAmount)
                            self.buy_order_book=self.order_book
                        self.nonPendingSell=True
                    elif self.nonPendingBuy or self.order_book_has_changed(order_info, 'buy') :
                        print('order book has changed')
                        self.cancel_order( self.buy_order_id,order_info)
                        self.buy_order_id=self.initialize_order('buy', self.buyAmount)
                        self.buy_order_book=self.order_book            
                        self.nonPendingBuy=False
                    else:
                        print('nothing changed after 15s')
                else:
                    self.buy_order_id=self.initialize_order("buy", self.buyAmount)
                    self.buy_order_book=self.order_book
                    self.nonPendingBuy=False
 
            if self.sellAmount>0 and self.sellAmount*self.order_book.asks[0][0]>3.5:
                if self.is_order_pending(self.sell_order_id):
                    order_info=self.get_order(self.sell_order_id)
                    if self.order_executed(order_info):
                        executed_amount = self.get_executed_amount(order_info, self.symbol)
                        print(f"executed amount {executed_amount}")
                        executed_price=self.get_executed_price(order_info,self.symbol)
                        print(f"executed price {executed_price}")

                        fee=self.get_fee(order_info)
                        print(f"sell fee: {fee}")
                        print(f"buy amount was:{self.buyAmount}")
                        new_buy_amount_usdt= executed_amount*executed_price-fee
                        self.buyAmount += new_buy_amount_usdt/executed_price
                        print(f"new amount now is:{self.buyAmount}")
                        self.remove_from_buy_journal(executed_price,executed_amount)
                        print(f"Buy journal after removing from it:{self.buyJournal}")
                        self.sellAmount -= executed_amount
                        print(f"sell amount is: {self.sellAmount}")

                        if executed_amount >= 0.99999 * self.sellAmount:
                            self.sell_order_id=0
                            self.sellAmount=0
                        else:
                            self.cancel_order( self.sell_order_id,order_info)
                            self.sell_order_id=self.initialize_order("sell", self.buyAmount)
                            self.sell_order_book=self.order_book
                        self.nonPendingBuy=True
                        return
                        
                    elif self.nonPendingSell or self.order_book_has_changed(order_info, 'sell')  :
                        self.cancel_order( self.sell_order_id,order_info)
                        self.sell_order_id=self.initialize_order('sell', self.sellAmount)
                        self.sell_order_book=self.order_book
                        self.nonPendingSell=False

                else:
                    self.sell_order_id=self.initialize_order("sell", self.sellAmount)
                    self.sell_order_book=self.order_book
                    self.nonPendingSell=False



    def get_price_accuracy(self):
        currency_pair_details = self.spot_api.get_currency_pair(self.symbol)
    
        return 10**(-1*currency_pair_details.precision)

    def calculate_max_buy_price(self):
        prices = self.spot_api.list_candlesticks(currency_pair=self.symbol, interval=self.interval, limit=self.limit)
        bands = taMan.TaMan().calculate_bollinger_bands(prices)
        lower = bands['lower_band']
        middle = bands['middle_band']
        return lower + 0.2 * (middle - lower)

    def calculate_min_sell_price(self):
        prices = self.spot_api.list_candlesticks(currency_pair=self.symbol, interval=self.interval, limit=self.limit)
        bands = taMan.TaMan().calculate_bollinger_bands(prices)
        upper = bands['upper_band']
        middle = bands['middle_band']
        return upper - 0.5 * (upper - middle)


    def find_target_price(self, order_book, order_type, limit_price):
            if order_type == 'buy':
   #             return 0, 0.002935
                for index, bid in enumerate(order_book.bids):
                    if bid[1] >= self.chase_amount and bid[0] < limit_price:
                        print(type(index))
                        print(type(bid[0]))
                        print(f"l'll place an order in {bid[0]}+{self.priceAccuracy}")
                        return index, float(Decimal(str(bid[0])) + Decimal(str(self.priceAccuracy)))  # Just above the target
            elif order_type == 'sell':
    #            return 0, 0.003042
                bought_price = self.get_purchased_price()
                for index, ask in enumerate(order_book.asks):
                    if ask[1] >= self.chase_amount and ask[0] > limit_price and ask[0] > bought_price * 1.01:
                        return index, float(Decimal(str(ask[0])) - Decimal(str(self.priceAccuracy)))  # Just below the target
            
            return None, None

    def execute_order(self, side, price, amount):
        visible_amount = self.get_visible_amount(amount)

        order = self.spot_api.create_order(
            order={"currency_pair":self.symbol,
            "side":side,
            "type":'limit',  
            "price":str(price),
            "amount":str(amount),
            "iceberg":str(visible_amount),}
        )
        print(f"Order creted: {side} {amount} at {price}")
    
        return order.id


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
        self.order_book=order_book
    def remove_order_from_book(self, type, price, amount):
            if type == 'buy':
                for index, bid in enumerate(self.order_book.bids):
                    if bid[0] == price:
                        bid[1] -= amount
                        if bid[1] <= 0:
                            del self.order_book.bids[index]
                        break
            elif type == 'sell':
                for index, ask in enumerate(self.order_book.asks):
                    if ask[0] == price:
                        ask[1] -= amount
                        if ask[1] <= 0:
                            del self.order_book.asks[index]
                        break
    def order_book_has_changed(self,order_info, type):
        if type == 'buy':
            for i in range(min(len(self.buy_order_book.bids), len(self.order_book.bids))):
                if self.order_book.bids[i][0] < order_info.price * 0.95:
                    break
                if self.buy_order_book.bids[i][0] != self.order_book.bids[i][0]:
                    return True
            return False
        elif type == 'sell':
            for i in range(min(len(self.sell_order_book.asks), len(self.order_book.asks))):
                if self.order_book.asks[i][0] > order_info.price * 1.05:
                    break
                if self.sell_order_book.asks[i][0] != self.order_book.asks[i][0]:
                    return True
            return False
        return False


    def cancel_order(self, order_id,order_info):
        while True:
            try:
                self.spot_api.cancel_order(order_id, self.symbol)
                print(f"Order {order_id} cancelled.")
                break

            except Exception as e:
                print(f"Failed to cancel order: {e}, l'll sleep for 15 seconds")
                time.sleep(15)
        self.remove_order_from_book(order_info.side,order_info.price,order_info.amount)

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
        index,price = self.find_target_price(self.order_book, order_type, limit_price)
        order_id = self.execute_order( order_type,  str(Decimal(str(price))), amount)
        self.update_order_book(self.order_book, order_type, index, price, amount)
        return order_id
        

    def order_executed(self, order_info):
        return order_info.fill_price > 0
 
    def get_executed_amount(self,order_info, symbol):
        return order_info.fill_price/order_info.price
    def get_executed_price(self,order_info, symbol):
        return order_info.price
    def get_fee(self,order_info): ##info in sell fee currency in usdt, in buy, fee currense in asset token
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

    
    def get_order(self, order_id):
        while True:
            try:
                order = self.spot_api.get_order(order_id, self.symbol)
                order.fill_price=float(order.fill_price)
                order.amount=float(order.amount)
                order.fee=float(order.fee)
                order.price=float(order.price)

                return order
            except Exception as e:
                print(f"Failed to fetch order info: {e} l'll retry after 15 seconds")
                time.sleep(15)
    def fetch_order_book(self):
        while True:
            try:
                order_book = self.spot_api.list_order_book(self.symbol, limit=100)
                for bid in order_book.bids:
                    bid[0]=float(bid[0])
                    bid[1]=float(bid[1])
                for ask in order_book.asks:
                    ask[0]=float(ask[0])
                    ask[1]=float(ask[1])

                return order_book
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
                time.sleep(15*60)

    def get_quote_amount(self,base_amount):
        return 1
    




    def get_visible_amount(self,total_amount):
        """
        Returns a random visible portion of an iceberg order,
        between 1/20 and 1/10 of the total order amount.
        
        Works with floats.
        """
        min_visible = total_amount / 20
        max_visible = total_amount / 10
        return round(random.uniform(min_visible, max_visible), 8) 
    

    def stop(self):
        print(f"Stopping trader for {self.symbol}")
        if self.buy_order_id != 0:
            self.spot_api.cancel_order(self.buy_order_id, self.symbol)
        if self.sell_order_id != 0:
            self.spot_api.cancel_order(self.sell_order_id, self.symbol)