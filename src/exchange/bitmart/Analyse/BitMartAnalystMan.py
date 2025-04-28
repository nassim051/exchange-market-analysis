import src.interface.Analyse.AbstractAnalystMan as AbstractAnalystMan
import src.exchange.bitmart.BitMartBasicDataMan as BasicDataMan
import src.exchange.bitmart.BitMartMarketMan as MarketMan
import src.exchange.bitmart.Analyse.BitMartWaveAnalyzer as BitMartWaveAnalyzer

class BitMartAnalystMan(AbstractAnalystMan.AbstractAnalystMan):
    def __init__(self, nbProcess, key=1):
        waveAnalyzer = BitMartWaveAnalyzer.BitMartWaveAnalyzer(
            nbHour=200,
            period=20,
            numProcess=1,
            numOfThreads=25,
            waveVolatility=5,
            timeFrame='hour4'
        )
        super().__init__(
            basicDataMan=BasicDataMan.BitMartBasicDataMan(),
            marketMan=MarketMan.BitMartMarketMan(),
            exchange='bitmart',
            secondOrMili=1000,
            nbProcess=nbProcess,
            waveAnalyzer=waveAnalyzer
        )

    def botIsTrue(self, pair):
        return 0

    def deleteFutures(self, pairs):
        listOfPairs = []
        for pair in pairs:
            listOfPairs.append(pair)
        for pair in pairs:
            prefix = pair.split('_')[0]
            if len(prefix) >= 3 and prefix[-1] in ('S', 'L') and prefix[-2].isdigit():
                listOfPairs.remove(pair)
        return listOfPairs
