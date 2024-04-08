# -*- coding:utf-8 -*-
# project name: project
# file name : BaseConfigMan
import src.exchange.lbank.APIV2Excu as APIV2Excu
import src.exchange.lbank.models.OrderBook as OrderBook
import src.exchange.lbank.models.Kline as Kline
import src.exchange.lbank.models.Transaction as Transaction
import src.interface.IMarketMan as IMarketMan
class MarketMan(IMarketMan.IMarketMan ):
    def __init__(self, key=1):
        self.excuReq=APIV2Excu.APIV2Excu(key)

    def getTicker(self,**d):
        str = self.getTicker.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        return self.excuReq.ExcuRequests( par, str )

    def getDepth(self,**d):
        str = self.getDepth.__name__
        d['size']=60
        d['merge']=0
        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]
        response=self.excuReq.ExcuRequests( par, str )
        response= OrderBook.editJsonResponse(response)
        if response==-1:
            print(f"The order book is empty or the bot is not availible for this: {d}")
        return response
    def getIncrDepth(self,**d):
        str = self.getIncrDepth.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        return self.excuReq.ExcuRequests( par, str )

    def getTrades(self,**d):
        str = self.getTrades.__name__+'v2'
        par = {}
        for key in d.keys():
            par[key] = d[key]
        response= self.excuReq.ExcuRequests(par, str)
        response=Transaction.editJsonResponse(response)
        return response


    def getKline(self,**d):
        str = self.getKline.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        response= self.excuReq.ExcuRequests( par, str )
        return Kline.editJsonResponse(response)




