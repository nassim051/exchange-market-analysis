import pprint

class Kline:
  
    def __init__( 
        self,temps,ouverture,high,low,close,volume,closeTime,quoteVolume,numOfTrades,takerBuyBaseVolume,takerBuyQuoteVolume):
        self.time=temps
        self.open=ouverture
        self.high=high
        self.low=low
        self.close=close
        self.volume=volume
        self.closeTime=closeTime
        self.quoteVolume=quoteVolume
        self.numOfTrades=numOfTrades
        self.takerBuyBaseVolume=takerBuyBaseVolume
        self.takerBuyQuoteVolume=takerBuyQuoteVolume
    def to_dict(self):
        return {
            "time":self.time,
            "open": self.open,
            "high": self.high,
            "low":self.low,
            "close":self.close,
            "volume":self.volume,
            "closeTime":self.closeTime,
            "quoteVolume":self.quoteVolume,
            "numOfTrades":self.numOfTrades,
            "takerBuyBaseVolume":self.numOfTrades,
            "takerBuyQuoteVolume":self.numOfTrades
        }
    
    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()
    
    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

@staticmethod
def editJsonResponse(response):
    if response==None:
        return -1
    edited_response=[]
    for res in response:
        edited_response.append(Kline(temps=res[0],ouverture=res[1],high=res[2],low=res[3],close=res[4],volume=res[5],closeTime=res[6],quoteVolume=res[7],numOfTrades=res[8],takerBuyBaseVolume=res[9],takerBuyQuoteVolume=res[10]))

    del(response)
    return edited_response
