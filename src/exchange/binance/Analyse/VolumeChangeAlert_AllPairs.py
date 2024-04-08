from src.db.DbManager import DbManager
from datetime import datetime, timedelta, timezone
import time
from date_time_event import Untiltime
import multiprocessing
import threading
from src.exchange.binance.binance_git.binance.spot import Spot
from src.exchange.binance.BinanceBasicDataMan import BinanceBasicDataMan


class VolumeChangeAlert_AllPairs:
    def __init__(self,interval,numProcess,numOfThreads):
        self.result = multiprocessing.Manager().dict()
        self.spot=Spot()
        self.basicDataMan=BinanceBasicDataMan()
        self.numProcess = numProcess
        self.numOfThreads=numOfThreads
        self.interval=interval #milliseconds
        self.greenRate=5
        self.redRate=-10
        self.yellowRate=10
        self.orangeRate=20
        self.sleep=0.8
        

    def startAnalyze(self,startTime,endTime):
        dbManager=DbManager()
        dbManager.renitialise('liquidity')
        symbols=[]
        for sym in self.basicDataMan.getAccuracyInfo()['symbols']:
            if sym['symbol'].endswith('USDT'):
                symbols.append(sym['symbol'])
        chunk_size = len(symbols) // self.numProcess
        processes = []

        for i in range(self.numProcess):
            start_index = i * chunk_size
            end_index = (i + 1) * chunk_size if i < self.numProcess - 1 else len(symbols)
            chunk = symbols[start_index:end_index]
            process = multiprocessing.Process(target=self.process_chunk, args=(chunk,startTime,endTime))
            processes.append(process)

        for process in processes:
            process.start()

        for process in processes:
            process.join()
        for symbol in self.result.keys():
                dbManager.insert_into_table("liquidity",(symbol,self.result[symbol]['nbGreen'],self.result[symbol]['nbYellow'],self.result[symbol]['nbOrange'],self.result[symbol]['nbRed'],self.result[symbol]['nbLastPositiveSignal'],self.result[symbol]['lastSignalColor']))

    def process_chunk(self, chunk,startTime,endTime):
        remaining_pairs = chunk[:]
        while remaining_pairs:
            num_threads = min(self.numOfThreads, len(remaining_pairs))
            threads = []
            for i in range(num_threads):
                pair = remaining_pairs.pop(0)
                thread = threading.Thread(target=self.calculateLiquidity, args=(pair,startTime,endTime))
                threads.append(thread)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()



  
    def calculateLiquidity(self,symbol,startTime,endTime):
            nbGreen=0
            nbYellow=0
            nbOrange=0
            nbRed=0
            nbLastPositiveSignal=0
            lastSignalColor=''
            volList=self.klineVolumeLast(symbol=symbol,startTime=startTime,timenow=endTime)
            if(len(volList)==0):
                return 
            prev_time=volList[0][0]
            prev_volume=volList[0][1]
            for i in range(len(volList)):
                current_time=volList[i][0]
                current_volume=volList[i][1]
                change_percentage = ((current_volume - prev_volume) / prev_volume) * 100            
                if (change_percentage > self.greenRate or change_percentage <self.redRate) and current_time-prev_time>=self.interval:
                    prev_time=current_time
                    prev_volume=current_volume
                    if change_percentage>self.orangeRate:
                        nbOrange+=1
                        nbLastPositiveSignal+=1
                        lastSignalColor='orange'
                    elif change_percentage>self.yellowRate:
                        nbYellow+=1
                        nbLastPositiveSignal+=1
                        lastSignalColor="yellow"
                    elif change_percentage>self.greenRate:
                        nbGreen+=1
                        nbLastPositiveSignal+=1
                        lastSignalColor="green"
                    elif change_percentage<=self.redRate:
                        nbRed+=1
                        nbLastPositiveSignal=0
                        lastSignalColor='red'
            self.result[symbol]={'nbGreen':nbGreen,'nbYellow':nbYellow,'nbOrange':nbOrange,'nbRed':nbRed,'nbLastPositiveSignal':nbLastPositiveSignal,'lastSignalColor':lastSignalColor}





    #klinvevolume2 for detectwhaltev3 
    def klineVolumeLast(self,timenow,symbol,startTime):
        volList=[]
        volume=0
        volumeBuy=0
        klineEndDate=timenow
        klineStartDate=int(startTime-timedelta(hours=24,minutes=1,seconds=30).total_seconds()*1000)
        while True:
            try:
                vol=self.spot.klines(limit=1000,symbol=symbol,startTime=klineStartDate,endTime=klineEndDate,interval='1s')
            except Exception as e:
                print(str(e))
                print("l'll sleep for 15 seconds")
                time.sleep(15)
            else:
                break
        if(len(vol)==0):
            return volList
        while int(vol[len(vol)-1][0])<timenow and len(vol)!=0:
            index=len(vol)-1
            print('call')
            while True:
                try:
                    result=self.spot.klines(limit=1000,symbol=symbol,startTime=vol[len(vol)-1][0]+1000,endTime=timenow,interval='1s')
                    vol+= result
                except Exception as e:
                    print(str(e))
                    print("l'll sleep for 15 seconds")
                    time.sleep(15)
                else:
                    break

            time.sleep(self.sleep)
        for v in vol:
            v[7]=float(v[7])
            v[9]=float(v[9])
        for i in range(3600*24):
            volume+=vol[i][7]
            volumeBuy+=vol[i][9]
        volList.append([vol[3600*24][0],volume,volumeBuy,float(vol[3600*24][1]),float(vol[3600*24][4])])
        for i in range(3600*24+1,len(vol)):
            volList.append([vol[i][0],volList[i-(3600*24+1)][1]-vol[i-(3600*24+1)][7]+vol[i-1][7],volList[i-(24*3600+1)][2]-vol[i-(24*3600+1)][9]+vol[i-1][9],float(vol[i][1]),float(vol[i][4])])#0:time,1:openPrice, 4:close price, 5:volume
            mtime=datetime.fromtimestamp(vol[i][0]/1000, tz = timezone.utc)+timedelta(hours=1)
            mtime=mtime.strftime('%Y-%m-%d %H:%M:%S')
        volDict={}
        print(f"Finished analyzing {symbol}")
        for v in volList:
            volDict[v[0]]=v[1]
        return volList
    def run(self,nbHours):
        endTime=int(datetime.now().timestamp())*1000
        startTime=int(endTime-timedelta(hours=nbHours).total_seconds()*1000)
        self.startAnalyze(startTime=startTime,endTime=endTime)




#create table liquidity(symbol STRING, nbGreen INTEGER, nbYellow INTEGER, nbOrange integer,nbRed Integer, nbLastPositiveSignal INTEGER, lastSignalColor STRING);
