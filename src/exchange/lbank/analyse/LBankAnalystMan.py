import pytest, os, sys, six, time
import src.interface.Analyse.AbstractAnalystMan as AbstractAnalystMan
import src.exchange.lbank.OrdersMan as OrderMan
import src.exchange.lbank.new_v2_inter.OrderMan as newOrderMan

import src.exchange.lbank.BasicDataMan as BasicDataMan
import src.exchange.lbank.MarketMan as MarketMan
from date_time_event import Untiltime
from datetime import datetime, timedelta

import src.Telegram.Telegram as Telegram
class LBankAnalystMan(AbstractAnalystMan.AbstractAnalystMan):
        def __init__(self,key=1):
                self.key=key
                super().__init__(BasicDataMan.BaseConfigMan(),MarketMan.MarketMan(),'LBank',1000,1)

 
        def deleteFutures(self, pairs):
            listOfPairs=[]
            for pair in pairs:
                listOfPairs.append(pair)
            for pair in pairs:
                prefix=pair.split('_')[0]
                if len(prefix)>=3 and prefix[-1] in ('s','l') and prefix[-2].isdigit():
                    listOfPairs.remove(pair)
            return listOfPairs
        

        def calculateBollinger(self, symbol, typ):
            time=bsdm.BaseConfigMan().getTimestamp()
            period=self.muchTypeWithPeriod(typ)
            size=20
            time=int(time['data']/1000-period*(size-1)*60)
            a=mm.MarketMan().getKline(symbol=symbol,size=size,type=typ,time=time)
            averagePrice=0
            for i in a['data']:
                averagePrice+=i[4]
            averagePrice/=20
            variance=0
            for i in a['data']:
                variance+=(i[4]-averagePrice)**2
            variance/=20
            ecartType=math.sqrt(variance)
            return averagePrice-2*ecartType, averagePrice ,averagePrice+2*ecartType


        def calculateMovingAverage(self, symbol, typ,size):
            time=bsdm.BaseConfigMan(self.key).getTimestamp()
            period=self.muchTypeWithPeriod(typ)
            time=int(time['data']/1000-period*(size-1)*60)
            a=mm.MarketMan(self.key).getKline(symbol=symbol,size=size,type=typ,time=time)
            averagePrice=0
            for i in a['data']:
                averagePrice+=i[4]
            averagePrice/=20
            return averagePrice
            
        def botIsTrue(self,pair):
            response=OrderMan.Orders(self.key).getOpenOrder(symbol=pair,current_page=1,page_length=15)
            bot=True
            if response['error_code']== 10008:
                bot=False
            return bot
        ###helper functions
        def muchTypeWithPeriod(self, period):
            if(period=='minute1'): return 1
            if(period=='minute5'): return 5
            if(period=='minute15'): return 15
            if(period=='minute30'): return 30
            if(period=='hour1'): return 60
            if(period=='hour4'): return 240
            if(period=='hour8'): return 480
            if(period=='hour12'): return 720
            if(period=='day1'): return 1440
            if(period=='week1'): return 1440*7
            if(period=='month1'): return 1440*30

                            
        def getPairsWithTheirVolume(self):
            pairsWithVolume={}
            data= mm.MarketMan(self.key).getTicker(symbol='all')
            data=data['data']
            for pair in data:
                pairsWithVolume[pair['symbol']]=pair['ticker']['vol']
            return pairsWithVolume

        def getFakeVolumeOfLbank(*symbol):
            if len(symbol)==1:
                data= mm.MarketMan(self.key).getTicker(symbol=symbol)
                data=data['data']
                return data[0]['ticker']['vol']
            listOfPair=mtp.pairList.importPairFromDb('symbol')
            for pair in listOfPair:
                print(pair[0])
            

        def turnToReadableDate(self,timestamp):
            readableDate = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return readableDate.split(' ')[1] ###returns only hh:mm:ss
        
        def  getTransactionHistory(self,sleep):
                volume=0
                telegram=Telegram.Telegram(channel=self.exchange)
                text=''
                orderMan=newOrderMan.OrderMan(key=3)
                old=self._turnDictByAsset(orderMan.getUser_info_account()['data']['balances'])
                while True:
                    time.sleep(sleep*60)
                    now=datetime.now()
                    while True:
                        result=orderMan.getUser_info_account()
                        if result.__contains__('data'):
                            new=self._turnDictByAsset(result['data']['balances'])
                            break
                        else:
                            time.sleep(15)

                    for asset in new.keys():
                        if asset not in old:
                            amount=float(new[asset]['free'])+float(new[asset]['locked'])
                            if asset=='usdt':
                                volume+=amount
                            text+=f"{asset}: new amount of {amount} bought\n"
                            break
                        if float(new[asset]['free'])+float(new[asset]['locked'])>float(old[asset]['free'])+float(old[asset]['locked']):
                            amount=float(new[asset]['free'])+float(new[asset]['locked'])-float(old[asset]['free'])-float(old[asset]['locked'])
                            if asset=='usdt':
                                volume+=amount
                            text+=f"{asset}: new amount of {amount} bought\n"

                        elif float(new[asset]['free'])+float(new[asset]['locked'])<float(old[asset]['free'])+float(old[asset]['locked']):
                            amount=float(old[asset]['free'])+float(old[asset]['locked'])-float(new[asset]['free'])-float(new[asset]['locked'])
                            if asset=='usdt':
                                volume+=amount
                            text+=f"{asset}: new amount of {amount} selled\n"
                    while True:
                        try:
                            if text!="":
                                text=f"{now}:\n{text} \nTotal volume: {volume}"
                                telegram.send_message(text)
                        except Exception:
                            print("Max telegram retries exceeded\nl'll sleep for 5 minutes and then try again")
                            time.sleep(300)
                        else:
                            break
                    text=''
                    old=new
        def _turnDictByAsset(self,myDict):
            newDict={}
            for data in myDict:
                newDict[data['asset']]={'free':data['free'],'locked':data['locked']}
            return newDict
        
        ###
            
