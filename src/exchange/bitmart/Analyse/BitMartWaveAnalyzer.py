import src.interface.Analyse.AbstractWaveAnalyzer as AbstractWaveAnalyzer
import src.exchange.bitmart.BitMartBasicDataMan as BasicDataMan
import src.exchange.bitmart.BitMartMarketMan as MarketMan

class BitMartWaveAnalyzer(AbstractWaveAnalyzer.AbstractWaveAnalyzer):
    def __init__(self, numProcess, numOfThreads, nbHour, timeFrame, waveVolatility, period, key=1):
        self.key = key
        super().__init__(
            size=1000,
            period=period,
            basicDataMan=BasicDataMan.BitMartBasicDataMan(),
            marketMan=MarketMan.BitMartMarketMan(),
            exchange='bitmart',
            secondOrMili=1,  
            numProcess=numProcess,
            numOfThreads=numOfThreads,
            nbHour=nbHour,
            timeFrame=timeFrame,
            waveVolatility=waveVolatility
        )

    def deleteFutures(self, pairs):
        listOfPairs = []
        for pair in pairs:
            listOfPairs.append(pair)
        for pair in pairs:
            prefix = pair.split('_')[0]
            if len(prefix) >= 3 and prefix[-1] in ('S', 'L') and prefix[-2].isdigit():
                listOfPairs.remove(pair)
        return listOfPairs
