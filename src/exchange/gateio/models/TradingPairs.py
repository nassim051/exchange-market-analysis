import pprint

class TradingPairs:
    def __init__( 
        self,
        id,
        base,
        quote,
        fee,
        min_base_amount,
        min_quote_amount,
        amount_precision,
        precision,
        trade_status,
        sell_start,
        buy_start,
    ):
        self.symbol = id
        self.base = base
        self.quote = quote
        self.fee = fee
        self.minTranQua = min_base_amount
        self.min_quote_amount = min_quote_amount
        self.quantityAccuracy = amount_precision
        self.priceAccuracy = precision
        self.trade_status = trade_status
        self.sell_start = sell_start
        self.buy_start = buy_start

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "base": self.base,
            "quote": self.quote,
            "fee": self.fee,
            "minTranQua": self.minTranQua,
            "min_quote_amount": self.min_quote_amount,
            "quantityAccuracy": self.quantityAccuracy,
            "priceAccuracy": self.priceAccuracy,
            "trade_status": self.trade_status,
            "sell_start": self.sell_start,
            "buy_start": self.buy_start,
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
    for item in response:
        edited_item = TradingPairs(
            id=item.id,
            base=item.base,
            quote=item.quote,
            fee=item.fee,
            min_base_amount=item.min_base_amount,
            min_quote_amount=item.min_quote_amount,
            amount_precision=item.amount_precision,
            precision=item.precision,
            trade_status=item.trade_status,
            sell_start=item.sell_start,
            buy_start=item.buy_start,
        )
        edited_response.append(edited_item)
    del(response)
    return edited_response
