import pytest, os, sys, six, time
import src.interface.Analyse.AbstractAnalystMan as AbstractAnalystMan
import src.exchange.gateio.GateBasicDataMan as BasicDataMan
import src.exchange.gateio.GateMarketMan as MarketMan
import src.exchange.gateio.github.gate_api.configuration as configuration
import src.exchange.gateio.github.gate_api.api_client as api_client
from date_time_event import Untiltime
from datetime import datetime
import src.Telegram.Telegram as Telegram
import src.exchange.gateio.Analyse.GateioWaveAnalyzer as GateioWaveAnalyzer

class GateioAnalystMan(AbstractAnalystMan.AbstractAnalystMan):
    def __init__(self,nbProcess,key=1):
        waveAnalyzer=GateioWaveAnalyzer.GateioWaveAnalyzer(nbHour=200,period=20,numProcess=1,numOfThreads=25,waveVolatility=5,timeFrame='hour4')


        super().__init__(basicDataMan=BasicDataMan.GateBasicDataMan(),marketMan=MarketMan.GateMarketMan(),exchange='gateio',secondOrMili=1,nbProcess=nbProcess,waveAnalyzer=waveAnalyzer)


    def botIsTrue(self,pair):
        return 0
    

    def deleteFutures(self, pairs):
        listOfPairs=[]
        for pair in pairs:
            listOfPairs.append(pair)
        for pair in pairs:
            prefix=pair.split('_')[0]
            if len(prefix)>=3 and prefix[-1] in ('S','L') and prefix[-2].isdigit():
                listOfPairs.remove(pair)
        return listOfPairs
    
    
    
    
    
    
