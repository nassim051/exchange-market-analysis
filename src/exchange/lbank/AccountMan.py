# -*- coding:utf-8 -*-
# project name: project
# file name : AccountMan
import src.exchange.lbank.APIV2Excu as APIV2Excu


class AccountMan:
    def __init__(self, key=1):
        self.excuReq = APIV2Excu.APIV2Excu(key)

    def getUserInfo(self,**d):

        str = self.getUserInfo.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        return self.excuReq.ExcuRequests( par, str )

    def genSubKey(self, **d):

        str = self.genSubKey.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]
        while True:
            try: 
                res=self.excuReq.ExcuRequests( par, str )
                res['data']
            except KeyError:
                print('key error in account men getsubkey retrying')
            else: 
                break
        return res['data']


    def refreshKey(self, **d):

        str = self.refreshKey.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        self.excuReq.ExcuRequests( par, str )


    def closeSubKey(self, **d):

        str = self.refreshKey.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        self.excuReq.ExcuRequests( par, str )

    def withdraw(self,**d):

        str = self.withdraw.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        self.excuReq.ExcuRequests( par, str )

    def cancelWithdraw(self,**d):

        str = self.withdraw.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        self.excuReq.ExcuRequests( par, str )

    def withdrawList(self,**d):

        str = self.withdraw.__name__

        par = {}
        for key in d.keys():
            par[ key ] = d[ key ]

        self.excuReq.ExcuRequests( par, str )