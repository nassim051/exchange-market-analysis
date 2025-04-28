from datetime import datetime, timedelta, timezone
import time,multiprocessing,threading
import src.db.DbManager as DbManager
from abc import ABC, abstractmethod
class AbstractWaveAnalyzer(ABC):
    TIMEFRAMES_TO_SECOND_MAP = {
    'minute1': int(timedelta(minutes=1).total_seconds()),
    'minute5': int(timedelta(minutes=5).total_seconds()),
    'minute15': int(timedelta(minutes=15).total_seconds()),
    'minute30': int(timedelta(minutes=30).total_seconds()),
    'hour1': int(timedelta(hours=1).total_seconds()),
    'hour4': int(timedelta(hours=4).total_seconds()),
    'hour8': int(timedelta(hours=8).total_seconds()),
    'hour12': int(timedelta(hours=12).total_seconds()),
    'day1': int(timedelta(days=1).total_seconds()),
    'week1': int(timedelta(weeks=1).total_seconds()),
    'month1': int(timedelta(days=30).total_seconds())  # Approximate
} 

    def __init__(self,basicDataMan,size ,marketMan,exchange,timeFrame, nbHour,waveVolatility,secondOrMili,period,numProcess,numOfThreads):
        self.result = multiprocessing.Manager().dict()
        self.marketMan= marketMan
        self.basicDataMan=basicDataMan
        self.exchange=exchange
        self.timeFrame=timeFrame
        self.nbHour=nbHour
        self.waveVolatility=waveVolatility
        self.secondOrMili=secondOrMili
        self.period=period
        self.numProcess=numProcess
        self.numOfThreads=numOfThreads
        self.sleep=0.6
        self.size=size
    def extractSymbols(self,result):
        symbols=[]
        if self.exchange=='binance':
            for res in result['symbols']:
                symbols.append(res['symbol'])
            return symbols
        for res in result:
            symbols.append(res.symbol)
        return symbols
    @abstractmethod
    def deleteFutures(result):
        pass
    def run(self,symbols=None,dbManager=None):
        if dbManager is None:
            dbManager=DbManager.DbManager()
        dbManager.renitialise('wave')
        if symbols is None:
            result=self.basicDataMan.getAccuracyInfo()
            result=self.extractSymbols(result)
            symbols=self.deleteFutures(result)
        chunk_size = len(symbols) // self.numProcess
        processes = []
        for i in range(self.numProcess):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size if i < self.numProcess - 1 else len(symbols)
            chunk = symbols[start_index:end_index]
            process = multiprocessing.Process(target=self.process_chunk, args=(chunk,))
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()
        for symbol in self.result.keys():
                dbManager.insert_into_table("wave",(symbol,self.exchange,self.result[symbol]['volatility'],self.result[symbol]['nbWave'],self.result[symbol]['averageAmplitude'],str(self.result[symbol]['listAmplitude'])))
 
    def process_chunk(self, chunk):
        remaining_pairs = chunk[:]
        while remaining_pairs:
            num_threads = min(self.numOfThreads, len(remaining_pairs))
            threads = []
            for i in range(num_threads):
                symbol = remaining_pairs.pop(0)
                thread = threading.Thread(target=self.analyseWave, args=(symbol,))
                threads.append(thread)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()





    def getLastPrice(self,symbol):
        klineEndDate=time.time()*self.secondOrMili
        klineStartDate=int(klineEndDate-timedelta(hours=self.nbHour).total_seconds()*self.secondOrMili)-self.TIMEFRAMES_TO_SECOND_MAP[self.timeFrame]*self.period*self.secondOrMili
        prices=self.marketMan.getKline(size=self.size,symbol=symbol,time=klineStartDate,type=self.timeFrame)
        if len(prices)==0:
            return prices
        while int(prices[len(prices)-1].time)+self.TIMEFRAMES_TO_SECOND_MAP[self.timeFrame]*self.secondOrMili<klineEndDate and len(prices)!=0:  
            time.sleep(self.sleep)
            result=self.marketMan.getKline(size=self.size,symbol=symbol,time=prices[len(prices)-1].time+self.TIMEFRAMES_TO_SECOND_MAP[self.timeFrame]*self.secondOrMili,type=self.timeFrame)
            if len(result)==0:
                return prices
            for res in result:
                prices.append(res)
        return self.restyleResult(prices)
    def restyleResult(self,result):
        new_result=[]
        for res in result:
            new_result.append({'time':res.time,'open':res.open,'high':res.high,'low':res.low,'close':res.close,'volume':res.volume})
        return new_result
        #getTicker
    def getPriceWithMa(self,symbol):
        prices=self.getLastPrice(symbol)
        return self.calculate_close_price_ma(prices,self.period)

    def calculate_close_price_ma(self,prices, period):
        if(len(prices)<self.period):
            return prices
        """
        Calculate the moving average based on the close prices for each element in the given list.

        Parameters:
        - prices (list): List of elements, each containing open, close, high, and low prices.
        - period (int): Period for the moving average.

        Returns:
        - list: List of tuples, each containing the close price and its corresponding moving average.
        """
        moving_averages = []

        for i in range(period - 1, len(prices)):
            close_prices = [element['close'] for element in prices[i - period + 1: i + 1]]
            ma_value = sum(close_prices) / period
            moving_averages.append({'time':prices[i]["time"],'open':prices[i]["open"],'high':prices[i]["high"],'low':prices[i]["low"],'close':prices[i]["close"],'volume':prices[i]["volume"],"ma":ma_value})
            
        return moving_averages

    def calculate_amplitude_percentages(self,prices):
        """
        Calculate the amplitude percentages for each element in the given list.

        Parameters:
        - prices (list): List of elements, each containing open, high, low, and close prices.

        Returns:
        - list: List of tuples, each containing the amplitude percentage for the corresponding element.
        """
        amplitude_percentages = []

        for price in prices:
            amplitude_percentage = ((price['high'] - price['low']) / price['low']) * 100
            amplitude_percentages.append(amplitude_percentage)    
        return sum(amplitude_percentages)/len(amplitude_percentages)
    

    def getPosition(self,price,ma):
        return 'up' if price > ma else 'down'
    

    def analyseWave(self,symbol):
        priceWithMa=self.getPriceWithMa(symbol=symbol)
        if(len(priceWithMa))<self.period:
            print(f"{symbol}: Insufficient price data for the selected period. Unable to calculate the moving average")
            return
        amplitude=self.calculate_amplitude_percentages(priceWithMa)
        currentPosition=self.getPosition(priceWithMa[0]['close'],priceWithMa[0]['ma'])
        nbWave=0
        minimum=priceWithMa[0]['low']
        maximum=priceWithMa[0]['high']
        amplitudeWaves = []
        while True:
            if currentPosition=='up':
                maximum=priceWithMa[0]['high']
                for i in range(1,len(priceWithMa)):
                    if priceWithMa[i]['high']>maximum:
                        maximum=priceWithMa[i]['high']
                    if(self.getPosition(priceWithMa[i]['low'],priceWithMa[i]['ma'])=='down'):
                        currentPosition='down'
                        break
                del(priceWithMa[:i])
                rate=(maximum-minimum)/minimum*100
                if(rate)>2:
                    nbWave+=1
                    amplitudeWaves.append(rate)
            if (len(priceWithMa)==1):
                break
            if currentPosition=='down':
                minimum=priceWithMa[0]['low']
                for i in range(1,len(priceWithMa)):
                    if priceWithMa[i]['low']<minimum:
                        minimum=priceWithMa[i]['low']
                    if(self.getPosition(priceWithMa[i]['high'],priceWithMa[i]["ma"])=='up'):
                        currentPosition='up'
                        break
                del(priceWithMa[:i])
                rate=(maximum-minimum)/minimum*100
                if(rate)>self.waveVolatility:
                    nbWave+=1
                    amplitudeWaves.append(rate)
            if (len(priceWithMa)==1):
                break
        if len(amplitudeWaves)==0:
            averageAmplitudeOfwaves=0
        else:
            averageAmplitudeOfwaves=sum(amplitudeWaves)/len(amplitudeWaves)
        self.result[symbol]={'volatility':amplitude,'nbWave':nbWave,'averageAmplitude':averageAmplitudeOfwaves,'listAmplitude':amplitudeWaves}
        print(f"{symbol}:")
        print(f"volatilité:{amplitude}")
        print(f"nbWave:{nbWave}")
        print(f"averageAmplitude of waves:{averageAmplitudeOfwaves}")
