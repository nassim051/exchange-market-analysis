import pytest, os, sys, six, time
import src.interface.Analyse.AbstractWaveAnalyzer as AbstracyWaveAnalyzer

import src.exchange.mexc.MexcBasicDataMan as BasicDataMan
import src.exchange.mexc.MexcMarketMan as MarketMan
from date_time_event import Untiltime
from datetime import datetime, timedelta

class MexcWaveAnalyzer(AbstracyWaveAnalyzer.AbstractWaveAnalyzer):
        def __init__(self,numProcess,numOfThreads,nbHour,timeFrame,waveVolatility,period,key=1):
                self.key=key
                super().__init__(period=period,basicDataMan=BasicDataMan.MexcBasicDataMan(),marketMan=MarketMan.MexcMarketMan,exchange='mexc',secondOrMili=1000,numProcess=numProcess,numOfThreads=numOfThreads,nbHour=nbHour,timeFrame=timeFrame,waveVolatility=waveVolatility)

        def deleteFutures(self, pairs):
            return pairs
