import pprint

class Kline:
    def __init__( 
        self,temps,volume,close,high,low,ouverture
    ):
        self.time=temps
        self.volume=volume
        self.close=close
        self.high=high
        self.low=low
        self.open=ouverture
        
        
    def to_dict(self):
        return {
            "time":self.time,
            "open": self.open,
            "high": self.high,
            "low":self.low,
            "close":self.close,
            "volume":self.volume
        }
    
    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()
    
    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

@staticmethod
def editJsonResponse(response):
    if response is None:
        return -1
    edited_response=[]
    for res in response:
        edited_response.append(Kline(temps=res[0],volume=res[1],close=res[2],high=res[3],low=res[4],ouverture=res[5]))
    del(response)
    return edited_response
