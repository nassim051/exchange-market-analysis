from types import SimpleNamespace
from src.interface.Analyse.AbstractAnalystMan import AbstractAnalystMan
from src.exchange.Xt.XtBasicDataMan import XtBasicDataMan
from src.exchange.Xt.XtMarketMan import XtMarketMan
from src.exchange.Xt.Analyse.XtWaveAnalyzer import XtWaveAnalyzer

class XtAnalystMan(AbstractAnalystMan):
    def __init__(self, nbProcess):
        waveAnalyzer = XtWaveAnalyzer(
            nbHour=200, period=20, numProcess=1, numOfThreads=25,
            waveVolatility=5, timeFrame='hour4'
        )
        super().__init__(
            basicDataMan=XtBasicDataMan(),
            marketMan=XtMarketMan(),
            exchange='xt',
            secondOrMili=1000,  # XT.com uses milliseconds
            nbProcess=nbProcess,
            waveAnalyzer=waveAnalyzer
        )

    def botIsTrue(self, pair):
        return 0

    def deleteFutures(self, pairs):
        # Remove futures or leveraged tokens if present
        filtered = []
        for pair in pairs:
            if not (pair.endswith("_PERP") or pair.endswith("_FUTURES") or '3L' in pair or '3S' in pair):
                filtered.append(pair)
        return filtered