import pprint

class TradingPairs:
    def __init__( 
        self,
        symbol,
        base,
        quoteAsset,
        makerCommission,
        quoteAmountPrecision,
        baseAssetPrecision,
        quoteAssetPrecision,
        status,
        
    ):
        self.symbol = symbol
        self.base = base
        self.quote = quoteAsset
        self.fee = makerCommission
        self.minTranQua = quoteAmountPrecision
        self.quantityAccuracy = baseAssetPrecision
        self.priceAccuracy = quoteAssetPrecision
        self.trade_status = status
        

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "base": self.base,
            "quote": self.quote,
            "fee": self.fee,
            "minTranQua": self.minTranQua,
            "quantityAccuracy": self.quantityAccuracy,
            "priceAccuracy": self.priceAccuracy,
            "trade_status": self.trade_status,
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
    for item in response['symbols']:
        edited_item = TradingPairs(
        symbol=item['symbol'],
        base=item['baseAsset'],
        quoteAsset=item['quoteAsset'],
        makerCommission=item['makerCommission'],
        quoteAmountPrecision=item['quoteAmountPrecision'],
        baseAssetPrecision=item['baseAssetPrecision'],
        quoteAssetPrecision=item['quoteAssetPrecision'],
        status=item['status']
        )
        edited_response.append(edited_item)
    del(response)
    return edited_response
