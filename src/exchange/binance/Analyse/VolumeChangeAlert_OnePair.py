from datetime import datetime, timedelta, timezone
import time
from src.exchange.binance.binance_git.binance.spot import Spot

class VolumeChangeAlert_OnePair:
    def __init__(self,interval):
        self.spot=Spot()
        self.interval=interval #milliseconds
        self.greenRate=5
        self.redRate=-10
        self.yellowRate=10
        self.orangeRate=20
        self.sleep=0.05        
    def updateToBtcRate(self):
        self.greenRate=0.5
        self.redRate=-0.5
        self.yellowRate=1
        self.orangeRate=2

    def detectWhaleLast3(self,symbol,startTime,endTime):
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
                    alert_type = "Increase" if current_volume>prev_volume  else "Decrease"
                    timeOfTrade=volList[i][0]
                    mtime = datetime.fromtimestamp(timeOfTrade/1000, tz = timezone.utc)+timedelta(hours=1)
                    mtime=mtime.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{mtime} volume change alert ({alert_type}) for {symbol}: {abs(change_percentage):.2f}% volume {current_volume} from {volList[i-1][4]} to {volList[i][4]}")                   
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






    #klinvevolume2 for detectwhaltev3 
    def klineVolumeLast(self,timenow,symbol,startTime):
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
        volList=[]
        volume=0
        volumeBuy=0
        nbCall=0
        if(len(vol)==0):
            return volList
        while int(vol[len(vol)-1][0])<timenow and len(vol)!=0:
            index=len(vol)-1
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
            nbCall+=1
            print(nbCall)
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
        for v in volList:
            volDict[v[0]]=v[1]

        return volList






    def run(self,symbol,nbHours):
        if symbol=='BTCUSDT':
            self.updateToBtcRate()
        endTime=int(datetime.now().timestamp())*1000
        startTime=int(endTime-timedelta(hours=nbHours).total_seconds()*1000)
        self.detectWhaleLast3(startTime=startTime,symbol=symbol,endTime=endTime)


