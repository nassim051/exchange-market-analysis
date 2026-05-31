import os
from configparser import ConfigParser
import src.exchange.lbank.client as client

class APIV2Excu:

    def __init__(self,key):
        configfile = u'./src/exchange/lbank/constant.ini'
        filePath = os.path.abspath(configfile)
        print("Looking for config file at:", filePath)  # <-- debug print

        self.config = ConfigParser()
        files_read = self.config.read(filePath)
        print("Files successfully read:", files_read)  # <-- debug print
        print("Sections found in the config:", self.config.sections())  # <-- debug print

        if key==1:
            self.apiKey=self.config.get("API","APIKEY")
            privKey=self.config.get("priveKey","PriveKey")
        elif key==2:
            self.apiKey=self.config.get("API","APIKEY2")
            privKey=self.config.get("priveKey","PriveKey2")
        elif key==3:
            self.apiKey=self.config.get("API","APIKEY3")
            privKey=self.config.get("priveKey","PriveKey3")
        elif key==4:
            self.apiKey=self.config.get("API","APIKEY4")
            privKey=self.config.get("priveKey","PriveKey4")
        elif key==5:
            self.apiKey=self.config.get("API","APIKEY5")
            privKey=self.config.get("priveKey","PriveKey5")
        
        self.privKey="-----BEGIN RSA PRIVATE KEY-----\n"+privKey+"\n-----END RSA PRIVATE KEY-----"
        self.signMethod=self.config.get("SIGNMETHOD","signmethod")
        self.excuReq=client.client()


    def ExcuRequests(self,par,str):
        url,me=self.config.get("URL",str).split(",")
        par["api_key"]=self.apiKey
        if self.signMethod=='RSA':
            res=self.excuReq.excuteRequestsRSA( par=par, url=url, method=me, privKey=self.privKey )
        else:
            res=self.excuReq.excuteRequestsHmac(par=par,url=url,method=me,secrtkey=self.secrtkey)
        return res
















