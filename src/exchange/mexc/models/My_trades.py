import pprint

class My_trades:
    def __init__( 
        self, symbol, create_time,order_id,side,role,price,amount
    ):
        self.id=symbol
        self.create_time=create_time
        self.order_id=order_id
        self.side=side
        self.role=role
        self.price=float(price)
        self.amount=float(amount)


    def to_dict(self):
        return {
            "symbol": self.symbol,
            "create_time": self.create_time,
            "price": self.price,
            "amount":self.amount,
            "side": self.side,
            "role": self.role,
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
        edited_item = My_trades(
            symbol=item.currency_pair,
            create_time=item.create_time,
            order_id=item.id,
            side=item.side,
            role=item.role,
            price=item.price,
            amount=item.amount,
        )
        edited_response.append(edited_item)
    del(response)
    return edited_response
