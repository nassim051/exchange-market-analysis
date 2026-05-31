import pytest, os, sys, six, time
import src.interface.Analyse.AbstractWaveAnalyzer as AbstractWaveAnalyzer

import src.exchange.gateio.GateBasicDataMan as BasicDataMan
import src.exchange.gateio.GateMarketMan as MarketMan
from date_time_event import Untiltime
from datetime import datetime, timedelta

class GateioWaveAnalyzer(AbstractWaveAnalyzer.AbstractWaveAnalyzer):
        def __init__(self,numProcess,numOfThreads,nbHour,timeFrame,waveVolatility,period,key=1,startDate=None,endDate=None):
                self.key=key
                super().__init__(size=1000,
                                 period=period,
                                 basicDataMan=BasicDataMan.GateBasicDataMan(),
                                 marketMan=MarketMan.GateMarketMan(),
                                 exchange='gateio',
                                 secondOrMili=1,
                                 numProcess=numProcess,
                                 numOfThreads=numOfThreads,
                                 nbHour=nbHour,
                                 timeFrame=timeFrame,
                                 waveVolatility=waveVolatility,
                                 startDate=startDate,
                                 endDate=endDate)

        # --- ADD THESE TWO METHODS TO FIX THE MULTIPROCESSING CRASH ---
        def __getstate__(self):
            state = self.__dict__.copy()
            # Remove the unpicklable API clients before passing 'self' to the new process
            if 'marketMan' in state:
                del state['marketMan']
            if 'basicDataMan' in state:
                del state['basicDataMan']
            return state

        def __setstate__(self, state):
            # Restore the standard attributes
            self.__dict__.update(state)
            # Re-initialize fresh API clients specifically for this new child process
            import src.exchange.gateio.GateBasicDataMan as BasicDataMan
            import src.exchange.gateio.GateMarketMan as MarketMan
            self.basicDataMan = BasicDataMan.GateBasicDataMan()
            self.marketMan = MarketMan.GateMarketMan()
        # --------------------------------------------------------------

        def deleteFutures(self, pairs):
            listOfPairs=[]
            for pair in pairs:
                listOfPairs.append(pair)
            for pair in pairs:
                prefix=pair.split('_')[0]
                if len(prefix)>=3 and prefix[-1] in ('S','L') and prefix[-2].isdigit():
                    listOfPairs.remove(pair)
            return listOfPairs