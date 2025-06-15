import pytest, os, sys, six, time
import src.interface.Analyse.AbstractAnalystMan as AbstractAnalystMan
from src.exchange.mexc.mexc_api_sdk.mexc_sdk.src.mexc_sdk import Spot
import src.exchange.mexc.MexcBasicDataMan as BasicDataMan
import src.exchange.mexc.MexcMarketMan as MarketMan
from date_time_event import Untiltime
from datetime import datetime, timedelta
import src.Telegram.Telegram as Telegram
import src.exchange.mexc.Analyse.MexcWaveAnalyzer as MexcWaveAnalyzer

class MexcAnalystMan(AbstractAnalystMan.AbstractAnalystMan):
    def __init__(self,nbProcess):
        waveAnalyzer=MexcWaveAnalyzer.MexcWaveAnalyzer(nbHour=200,period=20,numProcess=1,numOfThreads=25,waveVolatility=5,timeFrame='hour4')
        super().__init__(basicDataMan=BasicDataMan.MexcBasicDataMan(),marketMan=MarketMan.MexcMarketMan(),exchange='mexc',secondOrMili=1000,nbProcess=nbProcess,waveAnalyzer=waveAnalyzer)


    def botIsTrue(self,pair):
        return 0
    

    def deleteFutures(self, pairs):
        return pairs
    
    def  getTransactionHistory(self,sleep):
                volume=0
                telegram=Telegram.Telegram(channel=self.exchange)
                text=''
                spot=Spot(api_key='',api_secret='')
                old=self._turnDictByAsset(spot.account_info()['balances'])
                i=0
                while True:
                    i+=1
                    print(i)
                    time.sleep(sleep*60)
                    now=datetime.now()
                    while True:
                        while True:
                            try:
                                result=spot.account_info()
                            except Exception as e:
                                print('An exeption occured:'+str(e))
                                time.sleep(15)
                            else:
                                break
                        if len(result)!=0:
                            new=self._turnDictByAsset(result['balances'])
                            break
                        else:
                            time.sleep(15)
                    for asset in old.keys():
                        if asset not in new:
                            amount=float(old[asset]['free'])+float(old[asset]['locked'])
                            price=spot.avg_price(symbol=asset+'USDT')['price']                      
                            volume+=float(price)*float(amount)
                            text+=f"{asset}: new amount of {amount} selled\n"
                            
                    for asset in new.keys():
                        if asset not in old:
                            amount=float(new[asset]['free'])+float(new[asset]['locked'])
                            if asset!='USDT':
                                price=spot.avg_price(symbol=asset+'USDT')['price']                       
                                volume+=float(price)*float(amount)
                                text+=f"{asset}: new amount of {amount} bought\n"
                            continue
                        if float(new[asset]['free'])+float(new[asset]['locked'])>float(old[asset]['free'])+float(old[asset]['locked']):
                            amount=float(new[asset]['free'])+float(new[asset]['locked'])-float(old[asset]['free'])-float(old[asset]['locked'])
                            if asset!='USDT':
                                price=spot.avg_price(symbol=asset+'USDT')['price']
                                volume+=float(price)*float(amount)
                                text+=f"{asset}: new amount of {amount} bought\n"

                        elif float(new[asset]['free'])+float(new[asset]['locked'])<float(old[asset]['free'])+float(old[asset]['locked']):
                            amount=float(old[asset]['free'])+float(old[asset]['locked'])-float(new[asset]['free'])-float(new[asset]['locked'])
                            if asset!='USDT':
                                price=spot.avg_price(symbol=asset+'USDT')['price']
                                volume+=float(price)*float(amount)
                                text+=f"{asset}: new amount of {amount} selled\n"
                    while True:
                        try:
                            if text!="":
                                text=f"{now}:\n{text} \nTotal volume: {volume}"
                                telegram.send_message(text)
                        except Exception as e:
                            print('An exeption occured:'+str(e))                           
                            print("l'll sleep for 5 minutes and then try again")
                            time.sleep(300)
                        else:
                            break
                    text=''
                    old=new
    def getCgListOfPair(self,listOfPair):
            copy={}
            coingeckList=self.cg.get_coins_list()
            for data in coingeckList:
                copy[data["symbol"]]= data["id"]
            pairs={}
            for pair in listOfPair:
                try:
                    if len(pair.split('USDT'))==2:
                        pairs[pair]=copy[pair.split('USDT')[0].lower()]
                    elif len(pair.split('ETH'))==2:
                        pairs[pair]=copy[pair.split('ETH')[0].lower()]
                except:
                    continue
            return pairs
    
    def _turnDictByAsset(self,myDict):
        newDict={}
        for data in myDict:
            newDict[data['asset']]={'free':data['free'],'locked':data['locked']}
        return newDict
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
