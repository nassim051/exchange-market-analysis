import threading
import time
from datetime import datetime, timedelta
from . import OrderBookTrader  

class PairTradingController:
    def __init__(self,time_sleep=15*60,durationMinutes=None, initial_trader_params=None):
        """
        :param initial_trader_params: optional tuple of params for OrderBookTrader
        """
        self.traders = []
        self.lock = threading.Lock()
        if initial_trader_params:
            self._add_trader(*initial_trader_params)

        # Start the listener thread
        self.listener_thread = threading.Thread(target=self._listener, daemon=True)
        self.listener_thread.start()
        self.time_sleep = time_sleep
        self.durationMinute = durationMinutes

    def _add_trader(self, symbol, chase_amount, buyAmount=0, sellAmount=0,
                    interval="4h",strategy="down"):
        trader = OrderBookTrader.OrderBookTrader(
            symbol=symbol, chase_amount=chase_amount, buyAmount=buyAmount, sellAmount=sellAmount,
            interval=interval,strategy=strategy
        )
        with self.lock:
            self.traders.append(trader)
        print(f"[+] Trader added for symbol {symbol}")

    def _remove_trader(self, symbol):
        with self.lock:
            for trader in self.traders:
                if trader.symbol == symbol:
                    trader.stop()
                    self.traders.remove(trader)
                    print(f"[-] Trader removed for symbol {symbol}")
                    break
            else:
                print(f"[!] No trader found with symbol {symbol}")

    def _listener(self):
        while True:
            action = input("\nWhat do you want to do? (add / remove): ").strip().lower()
            if action == "add":
                try:
                    symbol = input("Symbol: ").strip()
                    chase_amount = float(input("Chase amount: "))
                    buyAmount = float(input("Buy amount (default 0): ") or 0)
                    sellAmount = float(input("Sell amount (default 0): ") or 0)
                    interval = input("Interval (default 4h): ") or "4h"
                    strategy = input("Strategy (default down) choose between down, range: ") or "range"

                    self._add_trader(symbol, chase_amount, buyAmount, sellAmount,
                                     interval,strategy)
                except Exception as e:
                    print(f"[!] Failed to add trader: {e}")
            elif action == "remove":
                symbol = input("Symbol to remove: ").strip()
                self._remove_trader(symbol)
            else:
                print("[!] Invalid action. Please type 'add' or 'remove'.")
    def stop_orders(self):
        # Implement logic to stop/cancel all active orders
        print("Stopping all orders...")
        # Example logic for cancelling orders
        for trader in self.traders:
            print(f"Cancelling order {trader}")
            trader.stop()

    def run(self):
        # Set end_time based on the provided duration, if given
        end_time = datetime.now() + timedelta(minutes=self.durationMinute) if self.durationMinute else None

        # Infinite loop if no duration is provided, else loop until end_time
        while True:
            # Check if we have an end_time set and if the current time is less than end_time
            if self.durationMinute and datetime.now() >= end_time:
                print("Duration reached, stopping the trader.")
                
                # Stop/cancel all orders before breaking
                self.stop_orders()

                # Break the loop after orders are stopped
                break
            with self.lock:
                active_traders = list(self.traders)  # avoid modifying list during iteration

            if not active_traders:
                print("[!] No traders active. Waiting 15 minutes before checking again.")
                time.sleep(15 * 60)
                continue

            sleep_per_trader = self.time_sleep / len(active_traders)
            for trader in active_traders:
                try:
                    trader.main()  
                except Exception as e:
                    print(f"[!] Error running trader {trader.symbol}: {e}")
                time.sleep(sleep_per_trader)

