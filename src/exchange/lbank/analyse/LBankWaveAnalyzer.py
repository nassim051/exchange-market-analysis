import pytest, os, sys, six, time
import src.interface.Analyse.AbstractWaveAnalyzer as AbstracyWaveAnalyzer

import src.exchange.lbank.BasicDataMan as BasicDataMan
import src.exchange.lbank.MarketMan as MarketMan
from date_time_event import Untiltime
from datetime import datetime, timedelta

class LBankWaveAnalyzer(AbstracyWaveAnalyzer.AbstractWaveAnalyzer):
        def __init__(self,numProcess,numOfThreads,nbHour,timeFrame,waveVolatility,period,key=1):
                self.key=key
                super().__init__(period=period,basicDataMan=BasicDataMan.BaseConfigMan(),marketMan=MarketMan.MarketMan(),exchange='lbank',secondOrMili=1,numProcess=numProcess,numOfThreads=numOfThreads,nbHour=nbHour,timeFrame=timeFrame,waveVolatility=waveVolatility)

 
        def deleteFutures(self, pairs):
            listOfPairs=[]
            for pair in pairs:
                listOfPairs.append(pair)
            for pair in pairs:
                prefix=pair.split('_')[0]
                if len(prefix)>=3 and prefix[-1] in ('s','l') and prefix[-2].isdigit():
                    listOfPairs.remove(pair)
            return listOfPairs
