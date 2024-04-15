from abc import abstractmethod
import src.db.DbManager as DbManager
from pycoingecko import CoinGeckoAPI
import time, multiprocessing
from date_time_event import Untiltime
from datetime import datetime, timedelta 
import copy

class AbstractAnalystMan:
    def __init__(self, basicDataMan, marketMan,exchange,secondOrMili,nbProcess):
        # Initialize common attributes or perform common tasks
        self.basicDataMan = basicDataMan
        self.marketMan= marketMan
        self.exchange=exchange
        self.cg = CoinGeckoAPI()
        self.secondOrMili=secondOrMili
        self.volume = multiprocessing.Manager().dict()
        #self.volume={}
        self.nbProcess=nbProcess
        self.process=[]
        for i in range(nbProcess):
            self.process.append({'basicDataMan':copy.copy(self.basicDataMan),'marketMan':copy.copy(self.marketMan)})
    
    @abstractmethod
    def botIsTrue(self,pair):
        pass


    def updatePairs(self):
        dataBase=DbManager.DbManager()
        pairList=self.basicDataMan.getAccuracyInfo()
        for pair in pairList:
            print(pair.symbol)
            dataBase.insert_into_table('pair',(pair.symbol,self.exchange,pair.quantityAccuracy,pair.minTranQua,pair.priceAccuracy))
            
    def findTokenWithGap(self):
            dataBase=DbManager.DbManager()
            listOfPair=dataBase.select_from_table('pair',['symbol'],[f"exchange ='{self.exchange}'"])
            listOfPair= self.simplifiate( listOfPair)
            listOfPair=self.deleteFutures(listOfPair)
            cgPairs= self.getCgListOfPair(listOfPair)
            shitPairs=[]
            for pair in listOfPair:
                orderBook=self.marketMan.getDepth(symbol=pair)
                if orderBook==-1 or len(orderBook.asks)<3 or len(orderBook.bids)<3 :
                    continue
                liquidity,ratio=self._calculSumOfOrderAndHumanActivityRatio(orderBook=orderBook)
                try:
                    pourcentageGap=self.getGap(orderBook.asks,orderBook.bids)
                except Exception as e:
                    print(f"exception occured")
                    print(str(e))
                    pourcentageGap=0.01
                if liquidity>100 and pourcentageGap > 0.01:
                    if pair in cgPairs:
                        cgVolume,marketCap,cgRank,listOnBinance,followers=self.getCgData(cgPairs[pair])
                    else:
                        cgVolume,marketCap,cgRank,listOnBinance,followers=None,None,None,False,None
                    bot = 1 if self.botIsTrue(pair) else 0
                    dataBase.insert_into_table('pairWithLiquidity',(pair,self.exchange, pourcentageGap, liquidity,cgVolume,marketCap,cgRank,listOnBinance, ratio, followers, bot))
                    print(pair,pourcentageGap)


    def calculVolume(self,symbol,timeNow,timeUnity,key):
        bookOrder=self.process[key-1]['marketMan'].getDepth(symbol=symbol)
        if bookOrder==-1:
            print(-1)
            return
        time.sleep(timeUnity)
        timeNow = str( timeNow.timestamp()*self.secondOrMili  ).split( "." )[ 0 ]
        transaction= self.process[key-1]['marketMan'].getTrades(symbol=symbol,size=600,time=timeNow )
        self.volume[symbol]['gap'].append(self.getGap(bookOrder.asks,bookOrder.bids))
        for order in bookOrder.asks:
                for trans in transaction:
                    if trans.price==float(order[0]) :
                        if trans.time<= int(timeNow)+timeUnity*1000  :# and trans['type']='buy'
                         self.volume[symbol]['asks']+=trans.price*trans.qty
                         self.volume[symbol]['volume']+=trans.price*trans.qty                    
                         self.volume[symbol]['transactions'].append({'direction':'asks','time':self.turnToReadableDate(trans.time/1000),'amount':trans.qty*trans.price, 'price':trans.price})
                         print(f"""We detect in {symbol} asks a trade of {trans.price*trans.qty} the price is {trans.price}\n volume: {self.volume[symbol]['volume']} asks: {self.volume[symbol]['asks']} bids:{self.volume[symbol]['bids']}""")
                         self.updateTransactionsWithGap(symbol,0.01)
        for order in bookOrder.bids:
                for trans in transaction :
                    if trans.price==float(order[0]) :
                        if  trans.time<= int(timeNow)+timeUnity*1000: # and trans['type']='sell'
                            self.volume[symbol]['bids']+=trans.price*trans.qty
                            self.volume[symbol]['volume']+=trans.price*trans.qty
                            self.volume[symbol]['transactions'].append({'direction':'bids','time':self.turnToReadableDate(trans.time/1000),'amount':trans.qty*trans.price, 'price':trans.price})
                            print(f"""We detect in {symbol} bids a trade of {trans.price*trans.qty} the price is {trans.price}\n volume: {self.volume[symbol]['volume']} asks: {self.volume[symbol]['asks']} bids:{self.volume[symbol]['bids']}""")
                            self.updateTransactionsWithGap(symbol,0.01)

    def createThread(self, nbOfFetch,timeUnity,addOnDb, symbol,key):
                dataBase=DbManager.DbManager()
                print(f"process number {key} symbol : {symbol}")
                self.volume={}
                for sym in symbol: 
                    self.volume[sym]={'volume': 0, 'gap':[],'asks': 0, 'bids': 0,'transactions':[],'nbTransactionGap':0,'volumeTransactionGap':0}
                nbOfTenUnit=int(nbOfFetch/10)
                for index in range(nbOfTenUnit):
                    timeNow=datetime.now()
                    threads=[]
                    for i in range(10):
                        for j in range(1,len(self.volume)+1):
                            th=Untiltime(self.calculVolume,timeNow+timedelta(0,timeUnity*i+1.5*j),args=(symbol[j-1],timeNow+timedelta(0,timeUnity*i+1.5*j),timeUnity,key))
                            th.start()
                            threads.append(th)  # Add the thread to the list            
                        #  print(f"{timeNow+timedelta(0,timeUnity*i+1.5*j)}  {symbol[j-1]}")
                    for th in threads:
                        th.join()
                    while True:
                        all_threads_finished = all(not th.is_alive() for th in threads)
                        if all_threads_finished:
                            break
                        time.sleep(60)
                if addOnDb==True:
                    oldSymbol=dataBase.select_from_table('volume4h',['symbol'],[f'exchange="{self.exchange}"'])
                    oldSymbol=dataBase.turnToList(oldSymbol)
                    for vol in self.volume.keys():
                        if oldSymbol.__contains__(vol)==False:
                            dataBase.insert_into_table('volume4h',(vol,self.exchange,0,0,0,0,0,0,""))
                    for vol in self.volume.keys():
                        gap=self.getGapFromVolume(self.volume[vol]['gap'])
                        dataBase.increment('volume4h',column='volume',newValue=str(self.volume[vol]['volume']),condition=[f"symbol='{vol}'",f"exchange='{self.exchange}'"])
                        dataBase.increment('volume4h',column='gap',newValue=gap,condition=[f"symbol='{vol}'",f"exchange='{self.exchange}'"])
                        dataBase.increment('volume4h',column='asks',newValue=str(self.volume[vol]['asks']),condition=[f"symbol='{vol}'",f"exchange='{self.exchange}'"])
                        dataBase.increment('volume4h',column='bids',newValue=str(self.volume[vol]['bids']),condition=[f"symbol='{vol}'",f"exchange='{self.exchange}'"])
                        dataBase.increment('volume4h',column='nbTransactionGap',newValue=str(self.volume[vol]['nbTransactionGap']),condition=[f"symbol='{vol}'",f"exchange='{self.exchange}'"])            
                        dataBase.increment('volume4h',column='volumeTransactionGap',newValue=str(self.volume[vol]['volumeTransactionGap']),condition=[f"symbol='{vol}'",f"exchange='{self.exchange}'"])                                   
                        dataBase.increment('volume4h',column='transactions',newValue='"'+str(self.volume[vol]['transactions'])+'"',condition=[f"symbol='{vol}'",f"exchange='{self.exchange}'"])            

    def countVolume(self,nbOfFetch,timeUnity,addOnDb, symbol=None):
        dataBase=DbManager.DbManager()
        if symbol is None:
            symbol=dataBase.select_from_table('pairwithliquidity',['symbol'],conditions=[f"exchange='{self.exchange}'","listOnBinance = false"])            
            symbol=dataBase.turnToList(symbol)
            symbolWIthVolume=dataBase.select_from_table('volume4h',['symbol'],conditions=[f"exchange='{self.exchange}'"])
            symbolWIthVolume=dataBase.turnToList(symbolWIthVolume)
            for sym in symbolWIthVolume:
                if sym in symbol:
                    symbol.remove(sym)
        while True:
            arguments=[]
            for i in range(self.nbProcess):
                arg=(nbOfFetch,timeUnity,addOnDb,symbol[0:30],i+1)
                symbol=symbol[30:]
                arguments.append(arg)   
            # Create four processes
            processes = []
            for args in arguments:
                process = multiprocessing.Process(target=self.createThread, args=(args[0],args[1],args[2],args[3],args[4]))
                processes.append(process)
                process.start()
                time.sleep(60)
            # Wait for all processes to finish
            for process in processes:
                process.join()
            print(f"End of the first loop here are the remaining symbols:\n{symbol}")
            if len(symbol)==0:
                break
        dataBase.close()




## helpers
    def getGapFromVolume(self,gaps):
        total=len(gaps)
        sum=0
        for gap in gaps:
            sum+=gap
        return sum/total if total!=0 else  0
    def getGap(self,asks,bids):
        sell=0
        buy=0
        for ask in asks:
            if ask[0] * ask[1] > 10 :
                sell = ask[0]  
                break
        for bid in bids:
            if bid[0] * bid[1] > 10:
                buy = bid[0]
                break
        return (sell-buy)/sell if(sell!=0 and buy!=0) else  0
    def _calculSumOfOrderAndHumanActivityRatio(self,orderBook):
        prix=[]
        ratio=0
        for i in range(min(10,len(orderBook.asks)-1)):
            prix.append(orderBook.asks[i][0]*orderBook.asks[i][1])
            gap=(orderBook.asks[i+1][1]-orderBook.asks[i][1])/orderBook.asks[i+1][1]
            if gap>=0.4:
                ratio+=1
        liquidity=sum(prix)    
        prix=[]
        for i in range(min(10,len(orderBook.bids)-1)):
            prix.append(orderBook.bids[i][0]*orderBook.bids[i][1])
            liquidity+=sum(prix)    
            liquidity/=2
            gap=(orderBook.bids[i+1][1]-orderBook.bids[i][1])/orderBook.bids[i+1][1]
            if gap>=0.4:
                ratio+=1
        return liquidity,ratio
    def getCgData(self,id):
        while True:
            try:
                response=self.cg.get_coin_by_id(id=id)
            except:
                print("coin geck serveur serveur latency, retrying after 10 seconds")
                time.sleep(10)
            else:
                break
        try:
            cgVolume=response["market_data"]['total_volume']['usd']
        except:
            cgVolume=-1
        try:
            marketCap=response["market_data"]['market_cap']['usd']
        except:
            marketCap=-1
        if self.exchange=='mexc':
            cgRank=-1
        else:
            cgRank=response['market_cap_rank']
        followers=response["community_data"]["twitter_followers"]
        listOnBinance=False
        for ticker in response['tickers']:
            if ticker['market']['name']=='Binance':
                listOnBinance=True
        return cgVolume,marketCap,cgRank,listOnBinance,followers
    
    def getCgListOfPair(self,listOfPair):
            copy={}
            coingeckList=self.cg.get_coins_list()
            for data in coingeckList:
                copy[data["symbol"]]= data["id"]
            pairs={}
            for pair in listOfPair:
                try:
                    pairs[pair]=copy[pair.split('_')[0].lower()]
                except:
                    continue
            return pairs
    def turnToReadableDate(self,timestamp):
        readableDate = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return readableDate.split(' ')[1] ###returns only hh:mm:ss

    def countTransactionsWithGap(self,transactions, gap,nbTransactionGap,volumeTransactionGap ):
        if len(transactions)==0:
            return nbTransactionGap,volumeTransactionGap
        oldPrice=transactions[0]['price']
        oldVolume=transactions[0]['amount']
        for trans in transactions:
            if oldPrice*(1+gap)<trans['price'] or oldPrice*(1-gap)>trans['price']:
                nbTransactionGap+=1
                volumeTransactionGap+=min(oldVolume,trans['amount'])*(abs(trans['price']-oldPrice))/oldPrice
            oldPrice=trans['price']
            oldVolume=trans['amount']
        return nbTransactionGap,volumeTransactionGap
    def updateTransactionsWithGap(self,symbol, gap ):
        transactions=self.volume[symbol]['transactions']
        if len(transactions)==0 or len(transactions)==1:
            return 
        oldPrice=transactions[len(transactions)-2]['price']
        oldVolume=transactions[len(transactions)-2]['amount']
        newPrice=transactions[len(transactions)-1]['price']
        newVolume=transactions[len(transactions)-1]['amount']
        if oldPrice*(1+gap)<newPrice or oldPrice*(1-gap)>newPrice:
            volumeAmount=min(oldVolume,newVolume)*(abs(newPrice-oldPrice))/oldPrice
            gapAmount=abs(oldPrice-newPrice)/oldPrice
            self.volume[symbol]['nbTransactionGap']+=1
            self.volume[symbol]['volumeTransactionGap']+=volumeAmount
            print(f"{symbol}:Strong transaction with a gap of {gapAmount} and volume of {volumeAmount}")
    
    def simplifiate(self, listOfPair):
        listOfPair = [symbol[0] for symbol in listOfPair]
        listOfPair = tuple(listOfPair)
        return listOfPair    
 