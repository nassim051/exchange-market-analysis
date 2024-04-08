#!/usr/bin/env python

import logging
import time
import json
from datetime import datetime, timedelta
from src.exchange.binance.binance_git.binance.spot import Spot
from src.exchange.binance.binance_git.binance.lib.utils import config_logging
from src.exchange.binance.binance_git.binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient

config_logging(logging, logging.DEBUG)

class WebSocketVolumeChangeAlert:
    def __init__(self,interval,symbol):
        self.prev_volume = None
        self.prev_time = None
        self.notif = []
        self.prev_price = None
        self.interval=interval
        if symbol=='BTCUSDT':
            self.goldenRate=0.5
        else:
            self.goldenRate=5
        self.symbol=symbol
    def message_handler(self, _, message):
        message = json.loads(message)
        if 'data' in message:
            current_volume = float(message['data']['q'])
            current_price = float(message['data']['c'])
            current_time = float(message['data']['E'])
            
            if self.prev_time and self.prev_volume is not None :
                change_percentage = ((current_volume - self.prev_volume) / self.prev_volume) * 100
                if current_time - self.prev_time >= self.interval and abs(change_percentage) > self.goldenRate:
                    alert_type = "Increase" if change_percentage > 0 else "Decrease"
                    mtime = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
                    logging.info(f" Volume change alert ({alert_type}) for {self.symbol}: {change_percentage}%. Volume:{current_volume} from {self.prev_price} to {current_price}")
                    self.notif.append({change_percentage: message, 'time': mtime})

                    volumeRecord = f"{mtime}: Volume change alert ({alert_type}) for {self.symbol}: {abs(change_percentage):.4f}%. Volume:{current_volume} from {self.prev_price} to {current_price}"
                    file_path = "volumeRecord.txt"

                    with open(file_path, "w") as file:
                        file.write(volumeRecord)
                    self.prev_volume = current_volume
                    self.prev_time = current_time
                    self.prev_price = current_price
            else:
                self.prev_volume = current_volume
                self.prev_time = current_time

    def run(self):
        my_client = SpotWebsocketStreamClient(on_message=self.message_handler, is_combined=True)
        my_client.ticker(symbol=self.symbol)
        time.sleep(3600 * 7.5)
        my_client.ticker(symbol=self.symbol, action=SpotWebsocketStreamClient.ACTION_UNSUBSCRIBE)
        time.sleep(5)
        logging.info("Closing WebSocket connection")
        my_client.stop()
        print(self.notif)

