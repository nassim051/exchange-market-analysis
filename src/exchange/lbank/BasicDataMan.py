# -*- coding:utf-8 -*-
# project name: project
# file name : BaseConfigMan
import src.exchange.lbank.APIV2Excu as APIV2Excu
import src.exchange.lbank.models.TradingPairs as TradingPairs

class BaseConfigMan:
    def __init__(self, key=1):

        self.excuReq=APIV2Excu.APIV2Excu(key)

    def getcurrencyPairs(self):
        str = self.getcurrencyPairs.__name__

        par = {}

        self.excuReq.ExcuRequests( par, str )

    def getAccuracyInfo(self):
        str = self.getAccuracyInfo.__name__
        par = {}


        response=self.excuReq.ExcuRequests( par, str )
        return TradingPairs.editJsonResponse(response)

    def getRatio(self,**d):
        str = self.getRatio.__name__

        par = {}

        self.excuReq.ExcuRequests( par, str )

    def getWithdrawConf(self,**d):
        str = self.getWithdrawConf.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        self.excuReq.ExcuRequests( par, str )

    def getTimestamp(self):
        str = self.getTimestamp.__name__

        par = {}

        return self.excuReq.ExcuRequests( par, str )

