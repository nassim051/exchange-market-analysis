import pprint

class OrderBook:
    def __init__( 
        self, id, current, update, asks, bids
    ):
        self.id = id
        self.current = current
        self.update = update
        for ask in asks:
            ask[0]=float(ask[0])
            ask[1]=float(ask[1])
        self.asks = asks
        for bid in bids:
            bid[0]=float(bid[0])
            bid[1]=float(bid[1])
        self.bids = bids

    def to_dict(self):
        return {
            "id": self.id,
            "current": self.current,
            "update": self.update,
            "asks": self.asks,
            "bids": self.bids,
        }
    
    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()
    
    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

@staticmethod
def editJsonResponse(response):
    edited_response = OrderBook(
    id=response.id,
    current=response.current,
    update=response.update,
    asks=response.asks,
    bids=response.bids
    )
    del(response)
    return edited_response
