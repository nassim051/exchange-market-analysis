from types import SimpleNamespace
from src.interface.Analyse.AbstractWaveAnalyzer import AbstractWaveAnalyzer
from src.exchange.Xt.XtBasicDataMan import XtBasicDataMan
from src.exchange.Xt.XtMarketMan import XtMarketMan

class XtWaveAnalyzer(AbstractWaveAnalyzer):
    def __init__(self, numProcess, numOfThreads, nbHour, timeFrame, waveVolatility, period):
        super().__init__(
            size=1000,
            period=period,
            basicDataMan=XtBasicDataMan(),
            marketMan=XtMarketMan(),
            exchange='xt',
            secondOrMili=1000,  # XT API uses milliseconds
            numProcess=numProcess,
            numOfThreads=numOfThreads,
            nbHour=nbHour,
            timeFrame=timeFrame,
            waveVolatility=waveVolatility
        )

    def deleteFutures(self, pairs):
        # Remove perpetual/futures contracts if present
        clean = []
        for p in pairs:
            if not (p.endswith("_PERP") or p.endswith("_FUTURES") or "/" in p):
                clean.append(p)
        return clean
