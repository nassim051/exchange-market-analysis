import pprint

class TradingPairs:
    def __init__(self, symbol, quantityAccuracy, minTranQua, priceAccuracy):
        self.symbol=symbol
        self.quantityAccuracy=quantityAccuracy
        self.minTranQua=minTranQua
        self.priceAccuracy=priceAccuracy
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "quantityAccuracy": self.quantityAccuracy,
            "minTranQua": self.minTranQua,
            "priceAccuracy": self.priceAccuracy,
        }
    
    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()
    
    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

@staticmethod
def editJsonResponse(response):
    edited_response = []
    for item in response['data']:
        edited_item = TradingPairs(            
            symbol=item["symbol"],
            minTranQua=item["minTranQua"],
            quantityAccuracy=item["quantityAccuracy"],
            priceAccuracy=item["priceAccuracy"],
            )
        edited_response.append(edited_item)
    del(response)
    return edited_response
