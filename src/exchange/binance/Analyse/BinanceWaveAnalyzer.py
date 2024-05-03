import pytest, os, sys, six, time
import src.interface.Analyse.AbstractWaveAnalyzer as AbstractWaveAnalyzer

import src.exchange.binance.BinanceBasicDataMan as BasicDataMan
import src.exchange.binance.BinanceMarketMan as MarketMan
from date_time_event import Untiltime
from datetime import datetime, timedelta

class BinanceWaveAnalyzer(AbstractWaveAnalyzer.AbstractWaveAnalyzer):
        def __init__(self,numProcess,numOfThreads,nbHour,timeFrame,waveVolatility,period,key=1):
                self.key=key
                super().__init__(size=1000,period=period,basicDataMan=BasicDataMan.BinanceBasicDataMan(),marketMan=MarketMan.BinanceMarketMan(),exchange='binance',secondOrMili=1000,numProcess=numProcess,numOfThreads=numOfThreads,nbHour=nbHour,timeFrame=timeFrame,waveVolatility=waveVolatility)

        def deleteFutures(self, pairs):
            symbols=[]
            for sym in pairs:
                if sym.endswith('USDT'):
                        symbols.append(sym)
            return symbols