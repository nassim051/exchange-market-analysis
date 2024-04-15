import pytest
import src.exchange.mexc.Analyse.MexcWaveAnalyzer as MexcWaveAnalyzer
#@pytest.mark.skip
def test_waveAnalyzer_analyseWave():
    waveAnalyzer=MexcWaveAnalyzer.MexcWaveAnalyzer(numProcess=1,numOfThreads=1,period=20,timeFrame="hour1",nbHour=48,waveVolatility=1.5)
    waveAnalyzer.run()
