# -*- coding:utf-8 -*-
# project name: project
# file name : ExcuHttp

import datetime
import hashlib
import random
import string
import time
from configparser import ConfigParser
import requests as req

import src.exchange.lbank.Util as Util


class client:

    def __init__(self):
        configfile=u'./src/exchange/lbank/constant.ini'

        cfg=ConfigParser()
        cfg.read(configfile)

        self.host=cfg.get("BASE","host")
        self.port=cfg.get("BASE","port")
        if self.port=='80':
            self.baseUrl=self.host
        else:
            self.baseUrl=self.host+":"+self.port

        self.util=Util.Util()


    def excuteRequestsRSA(self, par, url, method, privKey):
        '''execute requests with RSA signature'''
        urlstr=self.baseUrl+url

        num = string.ascii_letters + string.digits

        randomstr = "".join( random.sample( num, 35 ) )

        t = str( datetime.datetime.now().timestamp() * 1000 ).split( "." )[ 0 ]

        header = {"Accept-Language": 'zh-CN', "signature_method": 'RSA', 'timestamp': t, 'echostr': randomstr}

        par['echostr'] = randomstr

        sign = self.util.buildRSASignV2( params=par, privKey=privKey, t=t )

        par[ 'sign' ] = sign

        del par["signature_method"]
        del par["timestamp"]
        del par['echostr']


        #print('get response with header {h} and param {p} by {url}'.format(h=header,p=par,url=urlstr))
        while True:
            try:
                if method == 'post':
                    res = req.post( url=urlstr, data=par, headers=header,timeout=15 )
                else:
                    res = req.get( url=urlstr, params=par, headers=header, timeout=15 )
            except req.exceptions.ConnectionError as e :
                print('An exeption occured:'+str(e))
                print("connection error, let me sleep for 15 seconde")
                time.sleep(15)
            except req.exceptions.Timeout:
                print('An exeption occured:'+str(e))
                print('Request timeout, retrying after 15seconde')
                time.sleep(15)
            else:
                break

        if res.status_code == 200:
            resp = res.json()
           # print( resp )
            return resp
        else:
            print( res.status_code )

    def excuteRequestsHmac(self, par, url, method,secrtkey):
        '''execute requests with HmacSHA256 signature'''
        urlstr = self.baseUrl+url

        num = string.ascii_letters + string.digits
        randomstr = "".join(random.sample(num, 35))

        t = str( datetime.datetime.now().timestamp() * 1000 ).split( "." )[ 0 ]

        header = {"Accept-Language": 'zh-CN', "signature_method":"HmacSHA256", 'timestamp': t, 'echostr': randomstr}

        par[ 'echostr' ] = randomstr

        # sign = self.util.buildRSASignV2( params=par, privKey=privKey, t=t )
        sign=self.util.buildHmacSHA256(params=par,secrtkey=secrtkey,t=t)

        par[ 'sign' ] = sign

        del par["signature_method"]
        del par["timestamp"]
        del par['echostr']

       # print( 'get response with header {h} and param {p} by {url}'.format( h=header, p=par, url=urlstr ) )
        while True:
            try:
                if method == 'post':
                    res = req.post( url=urlstr, data=par, headers=header )
                else:
                    res = req.get( url=urlstr, params=par, headers=header )
            except req.exceptions.ConnectionError:
                print("connection error, let me sleep for 15 seconde")
                time.sleep(15)
            else:
                break
        if res.status_code == 200:
            resp = res.json()
            return resp
        else:
            print( res.status_code )


