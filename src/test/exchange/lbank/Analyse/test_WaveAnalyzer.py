import pytest
import src.exchange.lbank.analyse.LBankWaveAnalyzer as LBankWaveAnalyzer
import src.exchange.lbank.MarketMan as MarketMan
import src.exchange.lbank.BasicDataMan as BasicDataMan
@pytest.mark.skip
def test_waveAnalyzer_getLastPrice():
    marketMan=MarketMan.MarketMan()
    basicDataMan=BasicDataMan.BaseConfigMan()
    waveAnalyzer=AbstractWaveAnalyzer.AbstractWaveAnalyzer(basicDataMan=basicDataMan,marketMan=marketMan,period=20,exchange="LBank",timeFrame="hour1",nbDay=1,waveVolatility=0.2,secondOrMili=1)
    result=waveAnalyzer.getLastPrice(symbol="btc_usdt")
    print(result)
@pytest.mark.skip
def test_waveAnalyzer_getPriceWithMa():
    marketMan=MarketMan.MarketMan()
    basicDataMan=BasicDataMan.BaseConfigMan()
    waveAnalyzer=AbstractWaveAnalyzer.AbstractWaveAnalyzer(basicDataMan=basicDataMan,marketMan=marketMan,period=20,exchange="LBank",timeFrame="hour1",nbDay=1,waveVolatility=0.2,secondOrMili=1)
    result=waveAnalyzer.getPriceWithMa(symbol="btc_usdt")
    print(result)

@pytest.mark.skip
def test_waveAnalyzer_calculate_amplitude_percentages():
    marketMan=MarketMan.MarketMan()
    basicDataMan=BasicDataMan.BaseConfigMan()
    waveAnalyzer=AbstractWaveAnalyzer.AbstractWaveAnalyzer(basicDataMan=basicDataMan,marketMan=marketMan,period=20,exchange="LBank",timeFrame="hour1",nbDay=1,waveVolatility=0.2,secondOrMili=1)
    prices=waveAnalyzer.getLastPrice(symbol="btc_usdt")
    result=waveAnalyzer.calculate_amplitude_percentages(prices)
    print(result)

#@pytest.mark.skip
def test_waveAnalyzer_analyseWave():
    marketMan=MarketMan.MarketMan()
    basicDataMan=BasicDataMan.BaseConfigMan()   
    waveAnalyzer=LBankWaveAnalyzer.LBankWaveAnalyzer(numProcess=1,numOfThreads=1,period=20,timeFrame="hour1",nbHour=48,waveVolatility=1.5)
    waveAnalyzer.run()
